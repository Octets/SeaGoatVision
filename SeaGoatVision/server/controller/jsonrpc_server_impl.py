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
from SeaGoatVision.server.core.manager import Manager
import socket
import threading
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class Jsonrpc_server_impl():
    def __init__(self, port, host='localhost'):
        self.server = SimpleJSONRPCServer((host, port))
        self.manager = Manager()
        self.dct_observer = {}

    def register(self):
        # register all rpc callback
        self.server.register_function(self.close, "close")
        self.server.register_function(self.add_image_observer, "add_image_observer")
        self.server.register_function(self.set_image_observer, "set_image_observer")
        self.server.register_function(self.remove_image_observer, "remove_image_observer")
        self.server.register_function(self.get_params_media, "get_params_media")
        self.server.register_function(self.get_params_filterchain, "get_params_filterchain")
        
        self.server.register_function(self.manager.is_connected, "is_connected")
        self.server.register_function(self.manager.add_notify_server, "add_notify_server")
        self.server.register_function(self.manager.need_notify, "need_notify")
        self.server.register_function(self.manager.start_filterchain_execution, "start_filterchain_execution")
        self.server.register_function(self.manager.stop_filterchain_execution, "stop_filterchain_execution")
        self.server.register_function(self.manager.get_real_fps_execution, "get_real_fps_execution")
        self.server.register_function(self.manager.add_output_observer, "add_output_observer")
        self.server.register_function(self.manager.remove_output_observer, "remove_output_observer")
        self.server.register_function(self.manager.get_execution_list, "get_execution_list")
        self.server.register_function(self.manager.get_execution_info, "get_execution_info")
        self.server.register_function(self.manager.get_media_list, "get_media_list")
        self.server.register_function(self.manager.start_record, "start_record")
        self.server.register_function(self.manager.stop_record, "stop_record")
        self.server.register_function(self.manager.cmd_to_media, "cmd_to_media")
        self.server.register_function(self.manager.get_info_media, "get_info_media")
        self.server.register_function(self.manager.save_params_media, "save_params_media")
        self.server.register_function(self.manager.get_filterchain_list, "get_filterchain_list")
        self.server.register_function(self.manager.delete_filterchain, "delete_filterchain")
        self.server.register_function(self.manager.upload_filterchain, "upload_filterchain")
        self.server.register_function(self.manager.modify_filterchain, "modify_filterchain")
        self.server.register_function(self.manager.reload_filter, "reload_filter")
        self.server.register_function(self.manager.save_params, "save_params")
        self.server.register_function(self.manager.get_filter_list, "get_filter_list")
        self.server.register_function(self.manager.get_params_media, "get_filterchain_info")

    def run(self):
        self.server.serve_forever()

    def close(self):
        logger.info("Close jsonrpc server.")
        for observer in self.dct_observer.values():
            observer.close()
        self.manager.close()

    """

    def update_param(self, controller, request, done):
        logger.info("update_param request %s", str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            value = None
            if request.param.HasField("value_int"):
                value = request.param.value_int
            if request.param.HasField("value_bool"):
                value = request.param.value_bool
            if request.param.HasField("value_float"):
                value = request.param.value_float
            if request.param.HasField("value_str"):
                value = request.param.value_str
            try:
                response.status = not(self.manager.update_param(request.execution_name, request.filter_name, request.param.name, value))
            except Exception as e:
                response.status = 1
                response.message = e
        except Exception as e:
            log.printerror_stacktrace(logger, e)
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)
    """

    """
    def update_param_media(self, controller, request, done):
        logger.info("update_param_media request %s", str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            value = None
            if request.param.HasField("value_int"):
                value = request.param.value_int
            if request.param.HasField("value_bool"):
                value = request.param.value_bool
            if request.param.HasField("value_float"):
                value = request.param.value_float
            if request.param.HasField("value_str"):
                value = request.param.value_str
            try:
                response.status = not(self.manager.update_param_media(request.media_name, request.param.name, value))
            except Exception as e:
                response.status = 1
                response.message = e
        except Exception as e:
            log.printerror_stacktrace(logger, e)
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    """
    def get_params_filterchain(self, execution_name, filter_name):
        lst_param = self.manager.get_params_filterchain(execution_name, filter_name)
        return self._serialize_param(lst_param)

    def get_params_media(self, media_name):
        lst_param = self.manager.get_params_media(media_name)
        return self._serialize_param(lst_param)

    def _serialize_param(self, lst_param_obj):
        return [param.serialize() for param in lst_param_obj]

    ##########################################################################
    ############################## OBSERVATOR ################################
    ##########################################################################
    def add_image_observer(self, observer, execution_name, filter_name):
        """
        port = request.port
        try:
            observer = Observer(port)
            self.dct_observer[request.execution_name] = observer
            if self.manager.add_image_observer(observer.observer, request.execution_name, request.filter_name):
                response.status = 0
                observer.start()
            else:
                response.status = 1
                response.message = "This add_image_observer can't add observer."
        except Exception as e:
            log.printerror_stacktrace(logger, e)
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)
        """
    
    def set_image_observer(self, controller, request, done):
        logger.info("set_image_observer request %s", str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            observer = self.dct_observer.get(request.execution_name, None)
            if observer and self.manager.set_image_observer(observer.observer, request.execution_name, request.filter_name_old, request.filter_name_new):
                response.status = 0
            else:
                response.status = 1
                response.message = "This set_image_observer can't change observer."
        except Exception as e:
            log.printerror_stacktrace(logger, e)
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def remove_image_observer(self, controller, request, done):
        logger.info("remove_image_observer request %s", str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            observer = self.dct_observer.get(request.execution_name, None)
            if observer and self.manager.remove_image_observer(observer.observer, request.execution_name, request.filter_name):
                response.status = 0
            else:
                response.status = 1
                response.message = "This remove_image_observer can't remove observer."

        except Exception as e:
            log.printerror_stacktrace(logger, e)
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

        # close the socket
        observer = self.dct_observer.get(request.execution_name, None)
        if observer:
            observer.close()
            del self.dct_observer[request.execution_name]

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
