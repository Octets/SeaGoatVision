#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from SeaGoatVision.server.media.media_streaming import MediaStreaming
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons import log
import cv2
import thread
import zmq
import numpy as np

logger = log.get_logger(__name__)


class IPC(MediaStreaming):
    """
    Return image from IPC socket with ZeroMQ
    This media is a subscriber of ZeroMQ
    """
    key_ipc_name = "ipc name"

    def __init__(self, config):
        # Go into configuration/template_media for more information
        super(IPC, self).__init__()
        self.dct_params = {}
        self.config = Configuration()
        self.own_config = config
        self.media_name = config.name
        if config.device:
            self.device_name = config.device
        else:
            self.device_name = "/tmp/seagoatvision_media.ipc"
        self._is_opened = True
        self.run = True
        self.video = None

        self.context = zmq.Context()
        self.subscriber = None
        self.message = None

        self._create_params()
        self.deserialize(self.config.read_media(self.get_name()))

    def _create_params(self):
        self.dct_params = {}

        default_ipc_name = "ipc://%s" % self.device_name
        param = Param(self.key_ipc_name, default_ipc_name)
        param.add_notify_reset(self.open)
        self.dct_params[self.key_ipc_name] = param

    def serialize(self, is_config=False):
        return {self.key_ipc_name: self.dct_params.get(self.key_ipc_name).get()}

    def deserialize(self, data):
        if not data:
            return False
        if not isinstance(data, dict):
            log.print_function(
                logger.error, "Wrong format data, suppose to be dict into camera %s" %
                              self.get_name())
            return False
        res = data.get(self.key_ipc_name, None)
        if res:
            self.dct_params.get(self.key_ipc_name).set(res)
        return True

    def open(self):
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        device_name = self.dct_params.get(self.key_ipc_name).get()
        logger.info("Open media device %s" % device_name)
        self.subscriber.connect(device_name)
        thread.start_new_thread(self.fill_message, tuple())
        # call open when video is ready
        return MediaStreaming.open(self)

    def next(self):
        if not self.subscriber or not self.message:
            return None
        image = None
        message = self.message[:]
        self.message = None
        lst_pixel = list(bytearray(message))
        # the first 2 bytes is width of image
        len_message = len(lst_pixel) - 2
        if len_message:
            width = (lst_pixel[0] << 8) + lst_pixel[1]
            if not width:
                return None
            image = np.array(lst_pixel[2:])
            # check if missing pixel and replace by zero
            diff = len_message % width
            if diff:
                image += [0] * (width - diff)
            image = image.reshape((-1, width))
        shape = image.shape
        if len(shape) < 3 or 3 > shape[2]:
            # convert in 3 depth, bgr picture
            image_float = np.array(image, dtype=np.float32)
            vis2 = cv2.cvtColor(image_float, cv2.COLOR_GRAY2BGR)
            image = np.array(vis2, dtype=np.uint8)
        return image

    def close(self):
        MediaStreaming.close(self)
        # TODO need to debug, closing socket create errors and context.term freeze
        #self.subscriber.close()
        #self.context.term()
        self.subscriber = None
        return True

    def get_properties_param(self):
        return self.dct_params.values()

    def update_property_param(self, param_name, value):
        param = self.dct_params.get(param_name, None)
        if not param:
            return False
        param_value = param.get()
        if value == param_value:
            return True
        param.set(value)
        self.reload()
        return True

    def reset_property_param(self, param_name, value):
        self.reload()
        return True

    def fill_message(self):
        try:
            while self.subscriber:
                self.message = self.subscriber.recv()
        except zmq.ContextTerminated:
            pass
        finally:
            self.message = None
