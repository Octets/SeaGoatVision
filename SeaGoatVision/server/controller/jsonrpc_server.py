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

"""
Description : JsonRPC server implementation
"""

# Import required RPC modules
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from SeaGoatVision.server.core.cmdHandler import CmdHandler
from SeaGoatVision.commons import log
from SeaGoatVision.commons import keys
from SeaGoatVision.commons.param import Param
import cv2
from cv2 import cv

logger = log.get_logger(__name__)


class JsonrpcServer():
    def __init__(self, port):
        self.server = SimpleJSONRPCServer(('', port), logRequests=False)
        self.cmd_handler = CmdHandler()
        self.dct_observer = {}
        self.publisher = self.cmd_handler.get_publisher()

    def register(self):
        # register all rpc callback
        rf = self.server.register_function
        rf(self.add_image_observer, "add_image_observer")
        rf(self.set_image_observer, "set_image_observer")
        rf(self.remove_image_observer, "remove_image_observer")
        rf(self.get_params_media, "get_params_media")
        rf(self.get_param_media, "get_param_media")
        rf(self.get_params_filterchain, "get_params_filterchain")
        rf(self.get_param_filterchain, "get_param_filterchain")

        rf(self.cmd_handler.is_connected, "is_connected")
        rf(self.cmd_handler.start_filterchain_execution,
           "start_filterchain_execution")
        rf(self.cmd_handler.stop_filterchain_execution,
           "stop_filterchain_execution")
        rf(self.cmd_handler.get_fps_execution, "get_fps_execution")
        rf(self.cmd_handler.add_output_observer, "add_output_observer")
        rf(self.cmd_handler.remove_output_observer, "remove_output_observer")
        rf(self.cmd_handler.get_execution_list, "get_execution_list")
        rf(self.cmd_handler.get_execution_info, "get_execution_info")
        rf(self.cmd_handler.get_media_list, "get_media_list")
        rf(self.cmd_handler.start_record, "start_record")
        rf(self.cmd_handler.stop_record, "stop_record")
        rf(self.cmd_handler.cmd_to_media, "cmd_to_media")
        rf(self.cmd_handler.get_info_media, "get_info_media")
        rf(self.cmd_handler.save_params_media, "save_params_media")
        rf(self.cmd_handler.get_filterchain_list, "get_filterchain_list")
        rf(self.cmd_handler.delete_filterchain, "delete_filterchain")
        rf(self.cmd_handler.upload_filterchain, "upload_filterchain")
        rf(self.cmd_handler.modify_filterchain, "modify_filterchain")
        rf(self.cmd_handler.reload_filter, "reload_filter")
        rf(self.cmd_handler.save_params, "save_params")
        rf(self.cmd_handler.get_filter_list, "get_filter_list")
        rf(self.cmd_handler.get_filterchain_info, "get_filterchain_info")
        rf(self.cmd_handler.update_param_media, "update_param_media")
        rf(self.cmd_handler.update_param, "update_param")
        rf(self.cmd_handler.subscribe, "subscribe")

    def run(self):
        self.server.serve_forever()

    def close(self):
        logger.info("Close jsonrpc server.")
        self.cmd_handler.close()
        self.server.shutdown()

    def get_params_filterchain(self, execution_name, filter_name):
        lst_param = self.cmd_handler.get_params_filterchain(
            execution_name, filter_name)
        return self._serialize_param(lst_param)

    def get_param_filterchain(self, execution_name, filter_name, param_name):
        param = self.cmd_handler.get_param_filterchain(
            execution_name, filter_name, param_name)
        return self._serialize_param(param)

    def get_params_media(self, media_name):
        lst_param = self.cmd_handler.get_params_media(media_name)
        return self._serialize_param(lst_param)

    def get_param_media(self, media_name, param_name):
        param = self.cmd_handler.get_param_media(media_name, param_name)
        return self._serialize_param(param)

    def _serialize_param(self, param_obj):
        if isinstance(param_obj, list):
            return [param.serialize() for param in param_obj]
        elif isinstance(param_obj, Param):
            return param_obj.serialize()
        else:
            return None

    #
    # OBSERVATOR ################################
    #
    def add_image_observer(self, execution_name, filter_name):
        key = keys.create_unique_exec_filter_name(execution_name, filter_name)
        observer = self._cb_send_image(key)
        if self.cmd_handler.add_image_observer(observer, execution_name,
                                               filter_name):
            if key not in self.dct_observer:
                self.dct_observer[key] = observer
            return True
        return False

    def set_image_observer(self, execution_name, filter_name_old,
                           filter_name_new):
        old_key = keys.create_unique_exec_filter_name(
            execution_name, filter_name_old)
        new_key = keys.create_unique_exec_filter_name(
            execution_name, filter_name_new)
        observer = self.dct_observer[old_key]
        new_observer = self._cb_send_image(new_key)
        if self.cmd_handler.set_image_observer(observer,
                                               execution_name,
                                               filter_name_old,
                                               filter_name_new,
                                               new_observer=new_observer):
            del self.dct_observer[old_key]
            self.dct_observer[new_key] = new_observer
            return True
        return False

    def remove_image_observer(self, execution_name, filter_name):
        key = keys.create_unique_exec_filter_name(execution_name, filter_name)
        observer = self.dct_observer.get(key, None)
        if observer is None:
            logger.warning("Missing image observer : %s" % key)
        return self.cmd_handler.remove_image_observer(observer, execution_name,
                                                      filter_name)

    def _compress_cvmat(self, image):
        compress_img = cv2.imencode(
            ".jpeg", image, (cv.CV_IMWRITE_JPEG_QUALITY, 95))
        return compress_img[1].dumps()

    def _cb_send_image(self, key):
        def _publish_image(image):
            compress_cvmat = self._compress_cvmat(image)
            self.publisher.publish(key, compress_cvmat)

        return _publish_image
