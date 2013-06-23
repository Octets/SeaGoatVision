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
import logging

logger = logging.getLogger("seagoat")

class Firewire(Media_streaming):
    """Return images from a Firewire device."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        Media_streaming.__init__(self)
        self.config = Configuration()
        self.camera = None
        self.sleep_time = 1/15.0
        self.media_name = config.name
        try:
            ctx = video1394.DC1394Context()
        except:
            logger.error("Lib1394 is not supported.")
            return

        if config.guid:
            self.camera = ctx.createCamera(guid=config.guid)
        else:
            self.camera = ctx.createCamera(cid=config.no)

        if self.camera is not None:
            self.isOpened = True
        else:
            logger.warning("No Firewire camera detected.")

        self.shape = (800, 600)

        self.is_rgb = False
        self.is_mono = False
        self.is_format_7 = False
        self.actual_image = None

        self.deserialize(self.config.read_media(self.get_name()))

    def serialize(self):
        return [param.serialize() for param in self.get_properties_param()]

    def deserialize(self, data):
        if not data:
            return False
        for uno_data in data:
            if not uno_data:
                continue
            try:
                logger.debug("Deserialize param camera %s data: %s", self.get_name(), uno_data)
                param = Param(None, None, serialize=uno_data)
                self.update_property_param(param.get_name(), param.get())
            except Exception as e:
                logger.error("Deserialize: %s", e)
                return False
        return True

    def open(self):
        ctx = video1394.DC1394Context()
        camera = self.camera
        camera.resetBus()
        camera.isoSpeed = video1394.ISO_SPEED_400
        if self.is_format_7:
            # not supported
            camera.mode = video1394.VIDEO_MODE_FORMAT7_0
        elif self.is_rgb:
            camera.mode = video1394.VIDEO_MODE_800x600_RGB8
        elif self.is_mono:
            camera.mode = video1394.VIDEO_MODE_800x600_MONO8
        else:
            camera.mode = video1394.VIDEO_MODE_800x600_YUV422
        try:
            camera.framerate = video1394.FRAMERATE_15
        except:
            logger.warning("Framerate raise exception, but skip it from camera %s", self.get_name())
            # ignore it and use the default framerate
            pass

        camera.start(force_rgb8=True)
        camera.grabEvent.addObserver(self.camera_observer)
        # call open when video is ready
        Media_streaming.open(self)

    def camera_observer(self, im, timestamp):
        if self.is_rgb or not self.is_mono:
            image = Image.fromarray(im, "RGB")
            image2 = np.asarray(image, dtype="uint8")
            # transform it to bgr
            cv2.cvtColor(np.copy(image), cv.CV_BGR2RGB, image2)
        elif self.is_mono:
            image2 = im
        # shape = (im.shape[0], im.shape[1], 3)
        # rgb = np.zeros(shape, dtype=np.uint8)
        # np.copyto(rgb, im, casting="no")
        #self.notify_observer(image2)
        self.actual_image = image2

    def get_properties_param(self):
        lst_ignore_prop = ["Trigger"]
        lst_param = []
        dct_prop = self.camera.get_dict_available_features()
        for name, value in dct_prop.items():
            if name in lst_ignore_prop:
                continue
            try:
                if name == "White Balance":
                    param = Param("%s-auto" % name, False)
                    lst_param.append(param)
                    param = Param("%s-red" % name, value["RV_value"], min_v=value["min"], max_v=value["max"])
                    lst_param.append(param)
                    param = Param("%s-blue" % name, value["BU_value"], min_v=value["min"], max_v=value["max"])
                    lst_param.append(param)
                    continue
                elif name == "Shutter" or name == "Gain":
                    param = Param("%s-auto" % name, False)
                    lst_param.append(param)
                param = Param(name, value["value"], min_v=value["min"], max_v=value["max"])
                lst_param.append(param)
            except Exception as e:
                logger.error("get_properties_param: %s - name: %s, value: %s" % (e, name, value))
        return lst_param

    def update_property_param(self, param_name, value):
        auto = "-auto"
        if auto in param_name:
            param_name = param_name[:-len(auto)]
            if value:
                value = -1
            else:
                value = 0
        elif "White Balance" in param_name:
            if "red" in param_name:
                self.camera.set_whitebalance(RV_value=value)
            elif "blue" in param_name:
                self.camera.set_whitebalance(BU_value=value)
            else:
                logger.error("Can define the right color %s", param_name)
            return False
        logger.debug("Camera %s param_name %s and value %s", self.get_name(), param_name, value)
        self.camera.set_property(param_name, value)
        return True

    def next(self):
        return self.actual_image

    def close(self):
        Media_streaming.close(self)
        if self.camera:
            self.camera.stop()
            return True
        return False
