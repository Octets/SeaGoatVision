#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
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
try:
    from thirdparty.public.pydc1394 import video1394
except:
    pass
from SeaGoatVision.server.media.media_streaming import Media_streaming
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.configuration import Configuration
import numpy as np
import Image
import cv2
import cv2.cv as cv
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class Firewire(Media_streaming):
    """Return images from a Firewire device."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        super(Firewire, self).__init__()
        self.config = Configuration()
        self.camera = None
        self.dct_params = {}

        self.cam_guid = config.guid
        self.cam_no = config.no
        # the id is guid or no, writing into open_camera
        self.id = ""

        fps = 15
        self.sleep_time = 1 / 15.0
        self.media_name = config.name
        self.last_timestamp = -1
        self.actual_timestamp = -1
        self.count_not_receive = 0
        self.max_not_receive = fps * 2
        self.buffer_last_timestamp = False
        self.own_config = config

        if not self.open_camera():
            return

        self.shape = (800, 600)

        self.is_rgb = config.is_rgb
        self.is_mono = config.is_mono
        self.is_format_7 = config.is_format7
        self.is_yuv = config.is_yuv
        self.actual_image = None

        self._create_params()

        self.deserialize(self.config.read_media(self.get_name()))
        self.update_all_property()

    def _create_params(self):
        self.dct_params = {}
        if not self.camera:
            return
        lst_ignore_prop = ["Trigger"]
        dct_prop = self.camera.get_dict_available_features()
        for name, value in dct_prop.items():
            if name in lst_ignore_prop:
                continue
            try:
                if name == "White Balance":
                    param = Param("%s-auto" % name, False)
                    param.add_notify_reset(self.update_property_param)
                    self.dct_params[param.get_name()] = param
                    param = Param("%s-red" % name, value["RV_value"], min_v=value["min"], max_v=value["max"])
                    param.add_notify_reset(self.update_property_param)
                    self.dct_params[param.get_name()] = param
                    param = Param("%s-blue" % name, value["BU_value"], min_v=value["min"], max_v=value["max"])
                    param.add_notify_reset(self.update_property_param)
                    self.dct_params[param.get_name()] = param
                    continue
                elif name == "Shutter" or name == "Gain":
                    param = Param("%s-auto" % name, False)
                    param.add_notify_reset(self.update_property_param)
                    self.dct_params[param.get_name()] = param
                param = Param(name, value["value"], min_v=value["min"], max_v=value["max"])
                param.add_notify_reset(self.update_property_param)
                self.dct_params[param.get_name()] = param
            except Exception as e:
                log.printerror_stacktrace(logger, "%s - name: %s, value: %s" % (e, name, value))

    def serialize(self):
        return [param.serialize() for param in self.get_properties_param()]

    def is_opened(self):
        return self.camera is not None

    def deserialize(self, data):
        if not data:
            return False
        for uno_data in data:
            if not uno_data:
                continue
            try:
                param = Param(None, None, serialize=uno_data)
                own_param = self.dct_params.get(param.get_name(), None)
                if own_param:
                    own_param.merge(param)
            except Exception as e:
                log.printerror_stacktrace(logger, e)
                return False
        return True

    def initialize(self):
        if not self.camera:
            return False
        self.camera.initialize(reset_bus=True,
                               mode=self.own_config.mode,
                               framerate=self.own_config.framerate,
                               iso_speed=self.own_config.iso_speed,
                               operation_mode=self.own_config.operation_mode
                               )

    def open_camera(self):
        try:
            ctx = video1394.DC1394Context()
        except:
            log.print_function(logger.error, "Libdc1394 is not supported.")
            return False

        if self.cam_guid:
            self.camera = ctx.createCamera(guid=self.cam_guid)
            self.id = "guid %s" % str(self.cam_guid)
        else:
            self.camera = ctx.createCamera(cid=self.cam_no)
            self.id = "no %s" % str(self.cam_no)

        if self.camera is not None:
            return True
        else:
            log.print_function(logger.warning, "No Firewire camera detected - %s." % self.id)
        return False

    def open(self):
        if not self.camera:
            return False
        self.initialize()

        self.camera.start(force_rgb8=True)
        self.camera.grabEvent.addObserver(self.camera_observer)
        self.camera.stopEvent.addObserver(self.camera_close)
        # call open when video is ready
        Media_streaming.open(self)

    def camera_observer(self, im, timestamp):
        if self.is_rgb or not self.is_mono:
            image = Image.fromarray(im, "RGB")
            image2 = np.asarray(image, dtype="uint8")
            # transform it to BGR
            cv2.cvtColor(np.copy(image), cv.CV_BGR2RGB, image2)
        elif self.is_mono:
            image2 = im
        self.actual_image = image2
        self.last_timestamp = timestamp

    def camera_close(self):
        if not self.camera:
            # we already close the camera
            return
        # anormal close, do something!
        logger.error("Receive events camera close , retry to reopen it.")
        # clean camera
        self.camera.grabEvent.removeObserver(self.camera_observer)
        self.camera.stopEvent.removeObserver(self.camera_close)
        self.camera = None
        self.actual_image = None
        # reopen the camera
        if self.open_camera():
            self.open()
        else:
            logger.warning("Cannot find the camera")
            self.camera = None

    def get_properties_param(self):
        return self.dct_params.values()

    def update_all_property(self):
        for name, value in self.dct_params.items():
            self.update_property_param(name, value.get())

    def update_property_param(self, param_name, value):
        if not self.camera:
            return False

        auto = "-auto"
        if auto in param_name:
            new_param_name = param_name[:-len(auto)]
            logger.debug("Camera %s param_name %s and value %s", self.get_name(), param_name, value)
            self.camera.set_property_auto(new_param_name, value)
        elif "White Balance" in param_name:
            if "red" in param_name:
                self.camera.set_whitebalance(RV_value=value)
            elif "blue" in param_name:
                self.camera.set_whitebalance(BU_value=value)
            else:
                log.print_function(logger.error, "Can define the right color %s" % param_name)
                return False
        else:
            logger.debug("Camera %s param_name %s and value %s", self.get_name(), param_name, value)
            self.camera.set_property(param_name, value)
        return True

    def next(self):
        if not self.camera:
            return None

        diff_time = self.last_timestamp - self.actual_timestamp
        # logger.debug("actual time %s, last time %s, diff %s" % (self.actual_timestamp, self.last_timestamp, diff_time))
        self.actual_timestamp = self.last_timestamp
        if self.last_timestamp == -1:
            logger.warning("No image receive from %s" % (self.get_name()))
            return None
        if not diff_time:
            self.count_not_receive += 1
            if self.count_not_receive > self.max_not_receive:
                logger.error("Didn't receive since %d image. Restart the camera??")
                self.actual_timestamp = self.last_timestamp = -1
                self.count_not_receive = 0
                # TODO need to reload?
                self.reload()
                return None
            # ignore if only missing one image
            if not self.buffer_last_timestamp:
                self.buffer_last_timestamp = True
                return self.actual_image
            else:
                logger.warning("Receive no more image from %s, timestamp %d" % (self.get_name(), self.actual_timestamp))
                return None
        self.buffer_last_timestamp = False
        return self.actual_image

    def close(self):
        Media_streaming.close(self)
        if self.camera:
            self.camera.grabEvent.removeObserver(self.camera_observer)
            self.camera.stopEvent.removeObserver(self.camera_close)
            self.camera.stop()
            self.camera = None
            return True
        return False
