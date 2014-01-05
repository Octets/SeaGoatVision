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


def get_filter_original_name():
    return "-- original --"


def get_media_type_streaming_name():
    return "Streaming"


def get_media_type_video_name():
    return "Video"


def get_media_file_video_name():
    return "File"


def get_media_empty_name():
    return "Empty"


def get_empty_filterchain_name():
    return "-- empty filterchain --"


def get_empty_filter_name():
    return "-- empty filter --"


def get_key_media_play():
    return "play"


def get_key_media_pause():
    return "pause"


def get_key_media_loop():
    return "toggle_loop"


def set_key_media_frame():
    return "frame_media"

# generator

def create_unique_exec_filter_name(execution_name, filter_name):
    return "%s_%s" % (execution_name, filter_name)

# used by ZeroMQ


def get_key_execution_list():
    return "execution_list"


def get_key_filter_param():
    return "filter_param"


def get_key_media_param():
    return "media_param"


def get_key_all_output_filter():
    return "all_output_filter"


def get_lst_key_topic_pubsub():
    return {
        get_key_all_output_filter(): 1,
        get_key_execution_list(): 2,
        get_key_filter_param(): 3,
        get_key_media_param(): 4,
    }
