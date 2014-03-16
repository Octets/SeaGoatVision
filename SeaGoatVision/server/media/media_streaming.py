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

from media import Media
from SeaGoatVision.commons import keys
from recording.video_recorder import VideoRecorder
from recording.image_recorder import ImageRecorder
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class MediaStreaming(Media):

    def __init__(self):
        super(MediaStreaming, self).__init__()
        self._is_opened = False
        self.writer = None
        self.shape = None
        self.recorder_video = VideoRecorder(self)
        self.recorder_image = ImageRecorder(self)
        self.recorder = None

    def is_media_streaming(self):
        return True

    def is_media_video(self):
        return False

    def is_opened(self):
        return self._is_opened

    def get_info(self):
        info = super(MediaStreaming, self).get_info()
        if self.recorder:
            info["record_file_name"] = self.recorder.get_file_name()
        return info

    def get_type_media(self):
        return keys.get_media_type_streaming_name()

    def start_record(self, path=None, options={}):
        if type(options) != dict:
            options = {}
            logger.error("Wrong argument when start_record, receive options: %s" % options)

        if options.get("format", keys.get_key_format_avi()) == keys.get_key_format_png():
            self.recorder = self.recorder_image
        else:
            self.recorder = self.recorder_video
        compress = options.get("compress", 0)
        return self.recorder.start(self.shape, path=path, compress=compress)

    def stop_record(self):
        status = self.recorder.stop()
        self.recorder = None
        return status
