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

"""
Description : JsonRPC server implementation
"""

# Import required RPC modules
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from SeaGoatVision.server.core.cmdHandler import CmdHandler
import socket
import threading
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class Jsonrpc_server():
    def __init__(self, port, host='localhost'):
        self.server = SimpleJSONRPCServer((host, port), logRequests=False)
        self.cmdHandler = CmdHandler()
        self.dct_observer = {}

    def register(self):
        # register all rpc callback
        self.server.register_function(self.add_image_observer, "add_image_observer")
        self.server.register_function(self.set_image_observer, "set_image_observer")
        self.server.register_function(self.remove_image_observer, "remove_image_observer")
        self.server.register_function(self.get_params_media, "get_params_media")
        self.server.register_function(self.get_params_filterchain, "get_params_filterchain")

        self.server.register_function(self.cmdHandler.is_connected, "is_connected")
        self.server.register_function(self.cmdHandler.add_notify_server, "add_notify_server")
        self.server.register_function(self.cmdHandler.need_notify, "need_notify")
        self.server.register_function(self.cmdHandler.start_filterchain_execution, "start_filterchain_execution")
        self.server.register_function(self.cmdHandler.stop_filterchain_execution, "stop_filterchain_execution")
        self.server.register_function(self.cmdHandler.get_real_fps_execution, "get_real_fps_execution")
        self.server.register_function(self.cmdHandler.add_output_observer, "add_output_observer")
        self.server.register_function(self.cmdHandler.remove_output_observer, "remove_output_observer")
        self.server.register_function(self.cmdHandler.get_execution_list, "get_execution_list")
        self.server.register_function(self.cmdHandler.get_execution_info, "get_execution_info")
        self.server.register_function(self.cmdHandler.get_media_list, "get_media_list")
        self.server.register_function(self.cmdHandler.start_record, "start_record")
        self.server.register_function(self.cmdHandler.stop_record, "stop_record")
        self.server.register_function(self.cmdHandler.cmd_to_media, "cmd_to_media")
        self.server.register_function(self.cmdHandler.get_info_media, "get_info_media")
        self.server.register_function(self.cmdHandler.save_params_media, "save_params_media")
        self.server.register_function(self.cmdHandler.get_filterchain_list, "get_filterchain_list")
        self.server.register_function(self.cmdHandler.delete_filterchain, "delete_filterchain")
        self.server.register_function(self.cmdHandler.upload_filterchain, "upload_filterchain")
        self.server.register_function(self.cmdHandler.modify_filterchain, "modify_filterchain")
        self.server.register_function(self.cmdHandler.reload_filter, "reload_filter")
        self.server.register_function(self.cmdHandler.save_params, "save_params")
        self.server.register_function(self.cmdHandler.get_filter_list, "get_filter_list")
        self.server.register_function(self.cmdHandler.get_filterchain_info, "get_filterchain_info")
        self.server.register_function(self.cmdHandler.update_param_media, "update_param_media")
        self.server.register_function(self.cmdHandler.update_param, "update_param")
        self.server.register_function(self.cmdHandler.subscribe, "subscribe")

    def run(self):
        self.server.serve_forever()

    def close(self):
        logger.info("Close jsonrpc server.")
        for observer in self.dct_observer.values():
            observer.close()
        self.cmdHandler.close()
        self.server.shutdown()

    def get_params_filterchain(self, execution_name, filter_name):
        lst_param = self.cmdHandler.get_params_filterchain(execution_name, filter_name)
        return self._serialize_param(lst_param)

    def get_params_media(self, media_name):
        lst_param = self.cmdHandler.get_params_media(media_name)
        return self._serialize_param(lst_param)

    def _serialize_param(self, lst_param_obj):
        if lst_param_obj:
            return [param.serialize() for param in lst_param_obj]
        return []

    ##########################################################################
    ############################## OBSERVATOR ################################
    ##########################################################################
    def add_image_observer(self, port, execution_name, filter_name):
        observer = Observer(port)
        self.dct_observer[execution_name] = observer
        if self.cmdHandler.add_image_observer(observer.observer, execution_name, filter_name):
            observer.start()
            return True
        else:
            self._remove_image_observer(execution_name)
        return False

    def set_image_observer(self, execution_name, filter_name_old, filter_name_new):
        observer = self.dct_observer.get(execution_name, None)
        if observer and self.cmdHandler.set_image_observer(observer.observer, execution_name, filter_name_old, filter_name_new):
            return True
        return False

    def remove_image_observer(self, execution_name, filter_name):
        observer = self.dct_observer.get(execution_name, None)
        status = False
        if observer and self.cmdHandler.remove_image_observer(observer.observer, execution_name, filter_name):
            status = True
        self._remove_image_observer(execution_name)
        return status

    def _remove_image_observer(self, execution_name):
        # close the socket
        observer = self.dct_observer.get(execution_name, None)
        if observer:
            observer.close()
            del self.dct_observer[execution_name]

class Observer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", port))
        # self.add = (add, port)
        # self.socket.connect(self.add)
        self.__stop = False
        self.address = None

    def run(self):
        # waiting answer from client
        _, address = self.socket.recvfrom(1024)
        print address
        self.address = address
        self.buffer = 65507

    def observer(self, image):
        if self.address:
            data = image.dumps()
            nb_packet = int(len(data) / self.buffer) + 1
            # TODO missing count for index byte
            nb_char = 0
            for i in range(nb_packet):
                if not i:
                    sIndex = "b%d_" % nb_packet
                    begin_index = 0
                else:
                    sIndex = "c%d_" % i
                    begin_index += nb_char

                nb_char = self.buffer - len(sIndex)
                sData = "%s%s" % (sIndex, data[begin_index:begin_index + nb_char])
                try:
                    if not self.__stop:
                        self.socket.sendto(sData, self.address)
                    else:
                        break
                except Exception as e:
                    # Don't print error if we suppose to stop the socket
                    if not self.__stop:
                        logger.warning("Exception from image observer : %s", e)

    def close(self):
        self.__stop = True
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()
        self.socket = None
