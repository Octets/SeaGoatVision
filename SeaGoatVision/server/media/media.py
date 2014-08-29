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

from SeaGoatVision.server.core.pool_param import PoolParam
from thread_media import ThreadMedia
import numpy as np
from SeaGoatVision.commons import keys
from SeaGoatVision.commons import log
from SeaGoatVision.commons.param import Param
import json

logger = log.get_logger(__name__)


class MediaStatus(object):
    run = "run"
    close = "close"
    busy = "busy"
    pause = "pause"
    lst_status = [run, close, busy, pause]


class Media(PoolParam):
    def __init__(self):
        super(Media, self).__init__()
        # TODO change sleep_time dependant of real fps desire
        self.fps = 30.0
        self.sleep_time = 1 / self.fps
        self.lst_observer = []
        self.thread = None
        self.media_name = None
        self.active_loop = True
        self.is_client_manager = False
        # set publisher
        self._publisher = None
        self.status = None
        self.set_status(MediaStatus.close)
        # add generic param
        self._rotate_param = Param('angle', 0, max_v=3, min_v=0)
        desc = "Rotate the picture. 0 - 90 - 180 - 270"
        self._rotate_param.set_description(desc)
        self._rotate_param.add_group("Generic")

    def destroy(self):
        self.destroy_param()

    def set_publisher(self, publisher):
        self._publisher = publisher
        publisher.register("media.%s" % self.media_name)
        self._cb_publish = self._get_cb_publisher()

    def set_is_client_manager(self, is_client_manager):
        self.is_client_manager = is_client_manager

    def is_media_streaming(self):
        # complete it into media_streaming and media_video
        pass

    def is_media_video(self):
        # complete it into media_streaming and media_video
        pass

    def get_type_media(self):
        # complete it into media_streaming and media_video
        # type is Video or Streaming
        pass

    def get_name(self):
        return self.media_name

    def get_status(self):
        return self.status

    def set_status(self, status):
        if not status in MediaStatus.lst_status:
            msg = "Status %s in media %s not supported." % (status,
                                                            self.get_name())
            logger.error(msg)
            self.status = MediaStatus.close
        if self.status != status and self._cb_publish:
            self.status = status
            self._cb_publish({"status": status})

    def __iter__(self):
        return self

    def get_total_frames(self):
        return -1

    def get_info(self):
        fps = int(1 / self.sleep_time) if self.thread else -1
        return {
            "fps": fps,
            "nb_frame": self.get_total_frames(),
            "status": self.get_status()
        }

    def serialize(self, is_config=False):
        return super(Media, self).serialize(is_config=is_config)

    def deserialize(self, data):
        return super(Media, self).deserialize(data)

    def get_real_fps(self):
        if self.thread:
            return self.thread.get_fps()
        return -1

    def open(self):
        # IMPORTANT, if inherit, call this at the end
        # the thread need to be start when device is ready
        logger.info("Open media %s" % self.get_name())
        if self.is_client_manager:
            return True
        if self.thread:
            return False
        self.thread = ThreadMedia(self, self._cb_publish, self._rotate_param)
        self.thread.start()
        return True

    def next(self):
        # edit me in child
        pass

    def reset(self):
        # restore the media
        pass

    def close(self):
        logger.info("Close media %s" % self.get_name())
        self._remove_cb_publisher()
        self.stop_pooling_all_param()
        if self.is_client_manager:
            return True
        if not self.thread:
            return False
        self.thread.stop()
        self.thread = None
        self.status = MediaStatus.close
        return True

    def initialize(self):
        pass

    def reload(self, param=None):
        # TODO do observer and check parameter
        # ignore param_name and value, it's parameter from pool_param
        if not self.thread:
            return True
        status = self.close()
        if not status:
            return False
        # TODO force re-init filterchain
        self.initialize()
        return self.open()

    def change_sleep_time(self, sleep_time):
        self.sleep_time = sleep_time

    def add_observer(self, observer):
        start_media = False
        if not self.lst_observer:
            start_media = True
        self.lst_observer.append(observer)
        if start_media:
            self.open()

    def remove_observer(self, observer):
        if observer in self.lst_observer:
            self.lst_observer.remove(observer)
        else:
            logger.warning("Observer missing into media %s" % self.get_name())
        if not self.lst_observer:
            self.close()

    def notify_observer(self, image):
        # be sure the image is different for all observer
        for observer in self.lst_observer:
            observer(np.copy(image))

    def _add_notification_param(self, param):
        # send from publisher
        if not self._publisher:
            return
        data = {"media": self.media_name, "param": param.serialize()}
        json_data = json.dumps(data)
        self._publisher.publish(keys.get_key_media_param(), json_data)

    def set_loop_enable(self, enable):
        self.active_loop = enable

    def _get_cb_publisher(self):
        if not self._publisher:
            return
        key = self.get_name()
        return self._publisher.get_callback_publish("media.%s" % key)

    def _remove_cb_publisher(self):
        if not self._publisher:
            return
