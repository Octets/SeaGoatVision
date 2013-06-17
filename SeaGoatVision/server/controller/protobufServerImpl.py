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
Description : Server Service implementation using vServer_pb2, generate by .proto file
"""

# Import required RPC modules
from SeaGoatVision.proto import server_pb2
from SeaGoatVision.server.core.manager import Manager
import json
import socket
import threading

class ProtobufServerImpl(server_pb2.CommandService):
    def __init__(self, * args, ** kwargs):
        server_pb2.CommandService.__init__(self, * args, ** kwargs)
        self.manager = Manager()
        self.dct_observer = {}

    def close(self):
        print("Close protobuf.")
        for observer in self.dct_observer.values():
            observer.close()
        self.manager.close()

    ##########################################################################
    ################################ CLIENT ##################################
    ##########################################################################
    def is_connected(self, controller, request, done):
        print("is_connected request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        response.status = 0
        # We're done, call the run method of the done callback
        done.run(response)

    ##########################################################################
    ######################## EXECUTION FILTER ################################
    ##########################################################################
    def start_filterchain_execution(self, controller, request, done):
        print("start_filterchain_execution request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            # dont start a filterchain execution if it already exist
            response.status = int(not self.manager.start_filterchain_execution(request.execution_name,
                    request.media_name, request.filterchain_name, file_name=request.file_name))
            if response.status:
                response.message = "This filterchain_execution already exist."
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)


    def stop_filterchain_execution(self, controller, request, done):
        print("stop_filterchain_execution request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            response.status = int(not self.manager.stop_filterchain_execution(request.execution_name))
            if response.status:
                response.message = "This filterchain_execution is already close."
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    ##########################################################################
    ############################## OBSERVATOR ################################
    ##########################################################################
    def add_image_observer(self, controller, request, done):
        print("add_image_observer request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
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
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def set_image_observer(self, controller, request, done):
        print("set_image_observer request %s" % str(request).replace("\n", " "))

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
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def remove_image_observer(self, controller, request, done):
        print("remove_image_observer request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            observer = self.dct_observer.get(request.execution_name, None)
            if self.manager.remove_image_observer(observer.observer, request.execution_name, request.filter_name):
                response.status = 0
            else:
                response.status = 1
                response.message = "This remove_image_observer can't remove observer."


        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

        # close the socket
        observer = self.dct_observer.get(request.execution_name, None)
        if observer:
            observer.close()
            del self.dct_observer[request.execution_name]

    def add_output_observer(self, controller, request, done):
        print("add_output_observer request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            if self.manager.add_output_observer(request.execution_name):
                response.status = 0
            else:
                response.status = 1
                response.message = "This add_output_observer can't add observer."
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def remove_output_observer(self, controller, request, done):
        print("remove_output_observer request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            if self.manager.remove_output_observer(request.execution_name):
                response.status = 0
            else:
                response.status = 1
                response.message = "This remove_output_observer can't add observer."
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def get_params_filterchain(self, controller, request, done):
        print("get_params_filterchain request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.GetParamsFilterchainResponse()
        try:
            ret = self.manager.get_params_filterchain(request.execution_name, request.filter_name)
            if ret is not None:
                for item in ret:
                    if item.get_type() is int:
                        response.params.add(name=item.get_name(), value_int=item.get(), min_v=item.get_min(), max_v=item.get_max())
                    elif item.get_type() is bool:
                        response.params.add(name=item.get_name(), value_bool=item.get())
                    elif item.get_type() is float:
                        response.params.add(name=item.get_name(), value_float=item.get(), min_float_v=item.get_min(), max_float_v=item.get_max())
                    elif item.get_type() is unicode or item.get_type() is str:
                         response.params.add(name=item.get_name(), value_str=item.get())
        except Exception as e:
            print "Exception: ", e

        # We're done, call the run method of the done callback
        done.run(response)

    def get_execution_list(self, controller, request, done):
        print("get_execution_list request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.GetExecutionResponse()
        try:
            for execution in self.manager.get_execution_list():
                response.execution.append(execution)
        except Exception as e:
            print "Exception: ", e

        # We're done, call the run method of the done callback
        done.run(response)

    def get_execution_info(self, controller, request, done):
        print("get_execution_info request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.GetExecutionInfoResponse()
        try:
            o_exec = self.manager.get_execution_info(request.execution)
            response.filterchain = o_exec.filterchain
            response.media = o_exec.media
        except Exception as e:
            print "Exception: ", e

        # We're done, call the run method of the done callback
        done.run(response)

    ##########################################################################
    ################################ MEDIA ###################################
    ##########################################################################
    def get_media_list(self, controller, request, done):
        print("get_media_list request %s" % str(request).replace("\n", " "))

        response = server_pb2.GetMediaListResponse()
        for key, item in self.manager.get_media_list().items():
            response.media.append(key)
            response.type.append(item)

        done.run(response)

    def start_record(self, controller, request, done):
        print("start_record request %s" % str(request).replace("\n", " "))

        response = server_pb2.StatusResponse()
        response.status = int(not self.manager.start_record(request.media, path=request.path))

        done.run(response)

    def stop_record(self, controller, request, done):
        print("stop_record request %s" % str(request).replace("\n", " "))

        response = server_pb2.StatusResponse()
        response.status = int(not self.manager.stop_record(request.media))

        done.run(response)

    def cmd_to_media(self, controller, request, done):
        print("cmd_to_media request %s" % str(request).replace("\n", " "))

        response = server_pb2.StatusResponse()
        response.status = int(not self.manager.cmd_to_media(request.media_name, request.cmd))

        done.run(response)

    def get_info_media(self, controller, request, done):
        print("get_info_media request %s" % str(request).replace("\n", " "))

        response = server_pb2.GetInfoMediaResponse()
        value = self.manager.get_info_media(request.media_name)
        response.message = json.dumps(value)

        done.run(response)

    def get_params_media(self, controller, request, done):
        print("get_params_media request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.GetParamsMediaResponse()
        try:
            ret = self.manager.get_params_media(request.media_name)
            if ret is not None:
                for item in ret:
                    if item.get_type() is int:
                        response.params.add(name=item.get_name(), value_int=item.get(), min_v=item.get_min(), max_v=item.get_max())
                    elif item.get_type() is bool:
                        response.params.add(name=item.get_name(), value_bool=item.get())
                    elif item.get_type() is float:
                        response.params.add(name=item.get_name(), value_float=item.get(), min_float_v=item.get_min(), max_float_v=item.get_max())
                    elif item.get_type() is unicode or item.get_type() is str:
                         response.params.add(name=item.get_name(), value_str=item.get())
        except Exception as e:
            print "Exception: ", e

        # We're done, call the run method of the done callback
        done.run(response)

    def update_param_media(self, controller, request, done):
        print("update_param_media request %s" % str(request).replace("\n", " "))

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
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    ##########################################################################
    ############################### THREAD  ##################################
    ##########################################################################

    ##########################################################################
    ##########################  CONFIGURATION  ###############################
    ##########################################################################
    def get_filterchain_list(self, controller, request, done):
        print("get_filterchain_list request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.GetFilterChainListResponse()
        for item in self.manager.get_filterchain_list():
            if item.doc:
                response.filterchains.add(name=item.name, doc=item.doc)
            else:
                response.filterchains.add(name=item.name)

        # We're done, call the run method of the done callback
        done.run(response)

    ##########################################################################
    ############################ FILTERCHAIN  ################################
    ##########################################################################
    def get_filter_list_from_filterchain(self, controller, request, done):
        print("get_filter_list_from_filterchain request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.GetFilterListFromFilterChainResponse()
        for item in self.manager.get_filter_list_from_filterchain(request.filterchain_name):
            doc = item.doc
            if doc is None:
                doc = ""
            response.filters.add(name=item.name, doc=doc)

        # We're done, call the run method of the done callback
        done.run(response)

    def delete_filterchain(self, controller, request, done):
        print("delete_filterchain request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            response.status = int(not self.manager.delete_filterchain(request.filterchain_name))
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)


    def upload_filterchain(self, controller, request, done):
        print("upload_filterchain request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            response.status = int(not self.manager.upload_filterchain(request.filterchain_name, request.s_file_contain))
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)


    def modify_filterchain(self, controller, request, done):
        print("modify_filterchain request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            lstStrFilter = [filter.name for filter in request.lst_str_filters]
            response.status = int(not self.manager.modify_filterchain(request.old_filterchain_name, request.new_filterchain_name, lstStrFilter))
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)


    def reload_filter(self, controller, request, done):
        print("reload_filter request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            self.manager.reload_filter(request.filterName[0])
            response.status = 0
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def update_param(self, controller, request, done):
        print("update_param request %s" % str(request).replace("\n", " "))

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
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def save_params(self, controller, request, done):
        print("save_params request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            response.status = self.manager.save_params(request.execution_name)
        except Exception as e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)


    ##########################################################################
    ############################### FILTER  ##################################
    ##########################################################################
    def get_filter_list(self, controller, request, done):
        print("get_filter_list request %s" % str(request).replace("\n", " "))

        # Create a reply
        response = server_pb2.GetFilterListResponse()
        dct_filter = self.manager.get_filter_list()
        for filter in dct_filter.keys():
            response.filters.append(filter)
            response.doc.append(dct_filter[filter])

        # We're done, call the run method of the done callback
        done.run(response)


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
                        print(e)


    def close(self):
        self.__stop = True
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()
        self.socket = None

