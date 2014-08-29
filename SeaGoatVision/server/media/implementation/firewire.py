#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
#
# SeaGoatVision is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
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
from SeaGoatVision.server.media.media_streaming import MediaStreaming
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.configuration import Configuration
import numpy as np
from PIL import Image
import cv2
from cv2 import cv
from SeaGoatVision.commons import log
import time
import thread
import threading

logger = log.get_logger(__name__)


class Firewire(MediaStreaming):
    """Return images from a Firewire device."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        super(Firewire, self).__init__()
        self.config = Configuration()
        self.camera = None
        self.is_streaming = False
        self.loop_try_open_camera = False
        self.call_stop = False
        self.sem_closed = threading.Semaphore()

        self.cam_guid = config.guid
        self.cam_no = config.no
        # the id is guid or no, writing into open_camera
        self.id = ""
        self.key_auto_param = "-auto"
        self.reference_param = {"power": self._power,
                                "transmission": self._transmission}

        fps = 15
        self.sleep_time = 1 / 15.0
        self.media_name = config.name
        self.last_timestamp = -1
        self.actual_timestamp = -1
        self.count_not_receive = 0
        self.max_not_receive = fps * 2
        self.buffer_last_timestamp = False
        self.own_config = config
        self.is_rgb = config.is_rgb
        self.is_mono = config.is_mono
        self.is_format_7 = config.is_format7
        self.is_yuv = config.is_yuv
        self.actual_image = None
        self.shape = (800, 600)
        self.count_no_image = 0
        self.max_no_image = 120

        self.lst_param_shutter = []
        self.lst_param_whitebalance = []

        if not self.try_open_camera(repeat_loop=3, sleep_time=1):
            return

        self._create_params()

        self.deserialize(self.config.read_media(self.get_name()))
        self.update_all_property()

    def is_opened(self):
        return self.camera is not None

    def initialize(self):
        logger.debug("initialize camera %s" % self.get_name())
        if not self.camera:
            return False
        try:
            init = self.camera.initialize
            init(reset_bus=True, mode=self.own_config.mode,
                 framerate=self.own_config.framerate,
                 iso_speed=self.own_config.iso_speed,
                 operation_mode=self.own_config.operation_mode)
        except:
            return False
        return True

    def try_open_camera(
            self, open_streaming=False, repeat_loop=-1, sleep_time=1):
        # param :
        # int repeat_loop - if -1, it's an infinite loop, \
        # else it's the number loop
        # bool open_streaming - if true, try to start the streaming \
        # of seagoat and the firewire
        # can be use in threading or in init

        self.loop_try_open_camera = True
        while self.loop_try_open_camera:
            # need to wait 1 second if camera just shutdown, else it's crash
            time.sleep(sleep_time)
            if self.call_stop:
                return False
            # check if can access to the camera
            if self.open_camera():
                time.sleep(2)
                if self.initialize():
                    time.sleep(2)
                    if open_streaming:
                        time.sleep(2)
                        if self.open():
                            logger.debug(
                                "Open with success %s" %
                                self.get_name())
                            self.loop_try_open_camera = False
                            return True
                    else:
                        logger.debug("Finish with initialize")
                        self.loop_try_open_camera = False
                        return True
            # check if need to continue the loop
            if not repeat_loop:
                self.loop_try_open_camera = False
                return False
            if repeat_loop > 0:
                repeat_loop -= 1
            log.print_function(
                logger.error, "Cannot open the camera %s" %
                self.get_name())

    def open_camera(self):
        logger.debug("open camera %s" % self.get_name())
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
            log.print_function(
                logger.warning,
                "No Firewire camera detected - %s." %
                self.id)
        return False

    def open(self):
        logger.debug("open firewire %s" % self.get_name())
        self.call_stop = False
        if not self.camera:
            # try to open the camera
            # caution, can cause an infinite loop
            return self.try_open_camera(repeat_loop=3, open_streaming=True,
                                        sleep_time=1)

        self.camera.initEvent.addObserver(self.camera_init)
        self.camera.grabEvent.addObserver(self.camera_observer)
        # self.camera.stopEvent.addObserver(self.camera_closed)
        try:
            logger.debug("camera %s start." % self.get_name())
            self.camera.start(force_rgb8=True)
            self.param_transmission.set(True)
            logger.debug("camera %s start terminated." % self.get_name())
        except BaseException as e:
            logger.error(e)
            self.camera.stop()
            # something crash, restart the camera
            return self.try_open_camera(repeat_loop=1, open_streaming=True,
                                        sleep_time=1)
        return True

    def camera_init(self):
        MediaStreaming.open(self)
        self.is_streaming = True

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

    def camera_closed(self):
        self.sem_closed.acquire()
        if not self.camera or not self.is_streaming:
            # we already close the camera
            return
        # anormal close, do something!
        logger.error(
            "Receive events camera close %s, retry to reopen it." % self.id)
        # clean camera
        self.camera.grabEvent.removeObserver(self.camera_observer)
        # self.camera.stopEvent.removeObserver(self.camera_closed)
        self.actual_image = None
        # self.camera.safe_clean(free_camera=False)
        self.camera = None
        self.is_streaming = False
        # reopen the camera
        kwargs = {"open_streaming": True}
        # TODO how using kwargs???
        if not self.call_stop:
            thread.start_new_thread(self.try_open_camera, (True,))
            time.sleep(2)
        self.sem_closed.release()

    def next(self):
        if not self.camera or not self.is_streaming:
            return

        diff_time = self.last_timestamp - self.actual_timestamp
        # logger.debug("actual time %s, last time %s, diff %s" %
        # (self.actual_timestamp, self.last_timestamp, diff_time))
        self.actual_timestamp = self.last_timestamp
        if self.last_timestamp == -1:
            if not self.buffer_last_timestamp:
                self.buffer_last_timestamp = True
                return
                log.print_function(
                    logger.warning,
                    "No image receive from %s" % self.get_name())
            self.count_no_image += 1
            if self.count_no_image > self.max_no_image:
                self.count_no_image = 0
                self.camera_closed()
            return
        if not diff_time:
            self.count_not_receive += 1
            if self.count_not_receive >= self.max_not_receive:
                # logger.error("Didn't receive since %d images. Restart the
                # camera %s??" % (self.count_not_receive, self.id))
                logger.error(
                    "Didn't receive since %d images on camera %s" %
                    (self.count_not_receive, self.get_name()))
                self.actual_timestamp = self.last_timestamp = -1
                self.count_not_receive = 0
            # ignore if only missing one image
            if not self.buffer_last_timestamp:
                self.buffer_last_timestamp = True
                return self.actual_image
            else:
                # logger.warning(
                #    "Receive no more image from %s, timestamp %d" %
                #    (self.get_name(), self.actual_timestamp))
                return
        # reinitilize all protection
        self.buffer_last_timestamp = False
        self.count_no_image = 0
        self.count_not_receive = 0
        return self.actual_image

    def close(self):
        # Only the manager can call this close or the reload on media.py
        MediaStreaming.close(self)
        self.call_stop = True
        self.loop_try_open_camera = False
        self.is_streaming = False
        if self.camera:
            self.param_transmission.set(False)
            self.camera.stop()
            self.camera.initEvent.removeObserver(self.camera_init)
            self.camera.grabEvent.removeObserver(self.camera_observer)
            # self.camera.stopEvent.removeObserver(self.camera_closed)
            self.camera.safe_clean()
            self.camera = None
            return True
        else:
            logger.warning("Camera %s already close." % self.get_name())
        return False

    # PARAMS

    def _create_params(self):
        if not self.camera:
            return
        group_name_color = "Color"
        group_name_shutter = "Shutter"
        lst_ignore_prop = ["Trigger"]
        dct_prop = self.camera.get_dict_available_features()
        for name, value in dct_prop.items():
            if name in lst_ignore_prop:
                continue
            try:
                if name == "White Balance":
                    # add auto white balance
                    param = Param("%s%s" % (name, self.key_auto_param), False)
                    param.add_notify(self.update_property_param)
                    param.add_group(group_name_color)
                    param.add_notify(self._trig_auto_whitebalance)
                    self.add_param(param)
                    # add specific color of white balance
                    param = Param(
                        "RV_value",
                        value["RV_value"],
                        min_v=value["min"],
                        max_v=value["max"])
                    param.set_description("%s-red" % name)
                    param.add_notify(self.update_property_param)
                    param.add_group(group_name_color)
                    self.lst_param_whitebalance.append(param)
                    self.add_param(param)

                    param = Param(
                        "BU_value",
                        value["BU_value"],
                        min_v=value["min"],
                        max_v=value["max"])
                    param.set_description("%s-blue" % name)
                    param.add_notify(self.update_property_param)
                    self.lst_param_whitebalance.append(param)
                    param.add_group(group_name_color)
                    self.add_param(param)
                    continue

                param = Param(
                    name,
                    value["value"],
                    min_v=value["min"],
                    max_v=value["max"])
                param.add_notify(self.update_property_param)
                self.add_param(param)

                if name == "Shutter":
                    self.lst_param_shutter.append(param)
                    param.add_group(group_name_shutter)
                    # add auto param
                    param = Param("%s%s" % (name, self.key_auto_param), False)
                    param.add_notify(self._trig_auto_shutter)
                    param.add_notify(self.update_property_param)
                    param.add_group(group_name_shutter)
                    self.add_param(param)
            except BaseException as e:
                log.printerror_stacktrace(
                    logger, "%s - name: %s, value: %s" % (e, name, value))

        # add operational param
        group_operation = "operation"
        self.param_power = Param("Power", True)
        self.param_power.add_notify(self._power)
        self.param_power.add_group(group_operation)

        self.param_transmission = Param("Transmission", False)
        self.param_transmission.add_notify(self._transmission)
        self.param_transmission.add_group(group_operation)

        self.sync_params()

    def _trig_auto(self, param, lst_param, cb):
        if not self.camera:
            return False
        is_active = bool(param.get())
        for param in lst_param:
            # lock/unlock and start/stop pooling
            param.set_lock(is_active)
            if is_active:
                param.start_pooling(cb)
            else:
                param.stop_pooling()
        return True

    def _trig_auto_shutter(self, param):
        return self._trig_auto(param, self.lst_param_shutter, self._get_cam_property)

    def _trig_auto_whitebalance(self, param):
        return self._trig_auto(param, self.lst_param_whitebalance, self._get_cam_whitebalance_property)

    def _get_cam_property(self, param):
        return self.camera.get_property(param.get_name())

    def _get_cam_whitebalance_property(self, param):
        blue, red = self.camera.get_whitebalance()
        if "RV" in param.get_name():
            return red
        return blue

    def update_all_property(self):
        # If property is auto, don't apply manual parameter
        lst_auto = [value[:-(len(self.key_auto_param))]
                    for value in self.get_params().keys()
                    if self.key_auto_param in value]
        lst_auto = [value for value in lst_auto
                    if self.get_params("%s%s" %
                                       (value, self.key_auto_param)).get()]

        for key, param in self.get_params().items():
            contain_auto_variable = False
            # search active auto
            for active_key in lst_auto:
                if active_key in key:
                    contain_auto_variable = True
                    if self.key_auto_param in key:
                        self.update_property_param(param,
                                                   update_object_param=False)
            if contain_auto_variable:
                continue
            # find auto key disable and cancel it
            if self.key_auto_param in key:
                continue
            self.update_property_param(param, update_object_param=False)

    def update_property_param(self, param, update_object_param=True):
        if not self.camera or param.get_is_lock():
            return False
        param_name = param.get_name()
        value = param.get()

        if update_object_param:
            param.set(value)

        logger.debug(
            "Camera %s param_name %s and value %s",
            self.get_name(),
            param_name,
            value)
        if param_name.lower() in self.reference_param.keys():
            self.reference_param[param_name.lower()](param)
            return True

        if self.key_auto_param in param_name:
            new_param_name = param_name[:-len(self.key_auto_param)]
            self.camera.set_property_auto(new_param_name, value)
        elif "RV" in param_name:
            self.camera.set_whitebalance(RV_value=value)
        elif "BU" in param_name:
            self.camera.set_whitebalance(BU_value=value)
        else:
            self.camera.set_property(param_name, value)
        return True

    def _power(self, param):
        value = param.get()
        self.camera.power = int(bool(value))

    def _transmission(self, param):
        value = param.get()
        self.camera.transmission = int(bool(value))
