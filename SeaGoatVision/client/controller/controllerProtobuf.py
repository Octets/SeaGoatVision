#!/usr/bin/env python

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
Description : This controller use protobuf to communicate to the vision server
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

# Import required RPC modules
from SeaGoatVision.proto import server_pb2
import logging
import numpy as np
from protobuf.socketrpc import RpcService
import socket
import threading
from SeaGoatVision.commun.param import Param
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# The callback is for asynchronous call to RpcService
def callback(request, response):
    """Define a simple async callback."""
    log.info('Asynchronous response :' + response.__str__())

class ControllerProtobuf():
    def __init__(self, host, port, quiet=False):
        # Server details
        self.hostname = host
        self.port = int(port)
        self.quiet = quiet

        # Create a new service instance
        self.service = RpcService(server_pb2.CommandService_Stub, self.port, self.hostname)

        self.observer = {}

    def close(self):
        for observer in self.observer.values():
            observer.stop()
        print("Closed connection.")


    ##########################################################################
    ################################ CLIENT ##################################
    ##########################################################################
    def is_connected(self):
        if not self.quiet:
            print("Try connection")
        request = server_pb2.IsConnectedRequest()
        # Make an synchronous call
        response = None
        try:
            response = self.service.is_connected(request, timeout=10000) is not None
            if response and not self.quiet:
                print("Connection successful")
        except Exception as ex:
            log.exception(ex)

        return response

    ##########################################################################
    ######################## EXECUTION FILTER ################################
    ##########################################################################
    def start_filterchain_execution(self, execution_name, source_name, filterchain_name):
        """
            Start a filterchain on the server.
            Param : str - The unique execution name
                    str - The unique source name
                    str - The unique filterchain name
        """
        request = server_pb2.StartFilterchainExecutionRequest()
        request.execution_name = execution_name
        request.source_name = source_name
        request.filterchain_name = filterchain_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.start_filterchain_execution(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with start_filterchain_execution : %s" % response.message)
                    else:
                        print("Error with start_filterchain_execution.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def stop_filterchain_execution(self, execution_name):
        """
            Stop a filterchain on the server.
            Param : str - The unique execution name
        """
        request = server_pb2.StopFilterchainExecutionRequest()
        request.execution_name = execution_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.stop_filterchain_execution(request, timeout=10000)

            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with stop_filterchain_execution : %s" % response.message)
                    else:
                        print("Error with stop_filterchain_execution.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_params_filterchain(self, execution_name, filter_name):
        request = server_pb2.GetParamsFilterchainRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_params_filterchain(request, timeout=10000)

            if response:
                returnValue = []
                for param in response.params:
                    if param.HasField("value_int"):
                        returnValue.append(Param(param.name, param.value_int, min_v=param.min_v, max_v=param.max_v))
                    if param.HasField("value_bool"):
                        returnValue.append(Param(param.name, param.value_bool))
                    if param.HasField("value_str"):
                        returnValue.append(Param(param.name, param.value_str))
                    if param.HasField("value_float"):
                        returnValue.append(Param(param.name, param.value_float, min_v=param.min_float_v, max_v=param.max_float_v))
                    # TODO complete with other param restriction
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_execution_list(self):
        request = server_pb2.GetExecutionRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_execution_list(request, timeout=10000)

            if response:
                return response.execution
        except Exception as ex:
            log.exception(ex)

        return []

    def get_execution_info(self, execution_name):
        request = server_pb2.GetExecutionInfoRequest()
        request.execution = execution_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_execution_info(request, timeout=10000)
            if response:
                return response
        except Exception as ex:
            log.exception(ex)

        return None

    ##########################################################################
    ################################ SOURCE ##################################
    ##########################################################################
    def get_source_list(self):
        """
            Get the list for image provider.
        """
        request = server_pb2.GetSourceListRequest()
        # Make an synchronous call
        returnResponse = {}
        try:
            response = self.service.get_source_list(request, timeout=10000)
            if response:
                i = 0
                for key in response.source:
                    returnResponse[key] = response.type[i]
                    i += 1
            else:
                print("No answer on get_source_list")
        except Exception as ex:
            log.exception(ex)

        return returnResponse

    ##########################################################################
    ############################### THREAD  ##################################
    ##########################################################################

    ##########################################################################
    ##########################  CONFIGURATION  ###############################
    ##########################################################################

    ##########################################################################
    #############################  OBSERVER  #################################
    ##########################################################################
    def add_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name to select the filter
        """
        local_observer = self.observer.get(execution_name, None)
        if local_observer:
            print("This observer already exist")
            return False

        local_observer = Observer(observer, self.hostname, 5051)

        request = server_pb2.AddImageObserverRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.add_image_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with add_image_observer : %s" % response.message)
                    else:
                        print("Error with add_image_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        if not returnValue:
            local_observer.stop()
        else:
            self.observer[execution_name] = local_observer
            local_observer.start()

        return returnValue

    def set_image_observer(self, observer, execution_name, filter_name_old, filter_name_new):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name_old , filter to replace
                - string, filter_name_new , filter to use
        """
        observer = self.observer.get(execution_name, None)
        if not observer:
            print("This observer doesn't exist.")
            return False

        request = server_pb2.SetImageObserverRequest()
        request.execution_name = execution_name
        request.filter_name_old = filter_name_old
        request.filter_name_new = filter_name_new

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.set_image_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with set_image_observer : %s" % response.message)
                    else:
                        print("Error with set_image_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def remove_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name , filter to remove
        """
        observer = self.observer.get(execution_name, None)
        if not observer:
            print("This observer doesn't exist.")
            return False

        observer.stop()
        del self.observer[execution_name]

        request = server_pb2.RemoveImageObserverRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.remove_image_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with remove_image_observer : %s" % response.message)
                    else:
                        print("Error with remove_image_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)


        return returnValue

    def add_output_observer(self, execution_name):
        """
            attach the output information of execution to tcp_server
            supported only one observer. Add observer to tcp_server
        """
        request = server_pb2.AddOutputObserverRequest()
        request.execution_name = execution_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.add_output_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with add_output_observer : %s" % response.message)
                    else:
                        print("Error with add_output_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def remove_output_observer(self, execution_name):
        """
            remove the output information of execution to tcp_server
            supported only one observer. remove observer to tcp_server
        """
        request = server_pb2.RemoveOutputObserverRequest()
        request.execution_name = execution_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.remove_output_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with remove_output_observer : %s" % response.message)
                    else:
                        print("Error with remove_output_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    ##########################################################################
    ############################ FILTERCHAIN  ################################
    ##########################################################################
    def get_filterchain_list(self):
        """
            Return list of filter from filterchain.
        """
        request = server_pb2.GetFilterChainListRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filterchain_list(request, timeout=10000)
            if response:
                returnValue = response.filterchains
            else:
                print("Error : protobuf, get_filterchain_list response is None")

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_filter_list_from_filterchain(self, filterchain_name):
        """
            Return list of filter from filterchain.
        """
        request = server_pb2.GetFilterListFromFilterChainRequest()
        request.filterchain_name = filterchain_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filter_list_from_filterchain(request, timeout=10000)
            if response:
                returnValue = response.filters
            else:
                print("Error : protobuf, get_filterchain_list response is None")

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def delete_filterchain(self, filterchain_name):
        """
            deleter a filterchain
            Param : str - filterchain name
        """
        request = server_pb2.DeleteFilterChainRequest()
        request.filterchain_name = filterchain_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.delete_filterchain(request, timeout=10000)

            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with delete_filterchain : %s" % response.message)
                    else:
                        print("Error with delete_filterchain.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue

    def upload_filterchain(self, filterchain_name, s_file_contain):
        """
            upload a filterchain
            Param : str - filterchain name
                    str - the filterchain file
        """
        request = server_pb2.UploadFilterChainRequest()
        request.filterchain_name = filterchain_name
        request.s_file_contain = s_file_contain
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.upload_filterchain(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with upload_filterchain : %s" % response.message)
                    else:
                        print("Error with upload_filterchain.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue


    def modify_filterchain(self, old_filterchain_name, new_filterchain_name, lst_str_filters):
        """
            Edit or create a new filterchain
            Param : str - old_filterchain name
                    str - new_filterchain name
                    list - the list in string of filters
        """
        request = server_pb2.ModifyFilterChainRequest()
        request.old_filterchain_name = old_filterchain_name
        request.new_filterchain_name = new_filterchain_name
        for filter_name in lst_str_filters:
            request.lst_str_filters.add().name = filter_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.modify_filterchain(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with modify_filterchain : %s" % response.message)
                    else:
                        print("Error with modify_filterchain.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue

    def update_param(self, execution_name, filter_name, param_name, value):
        request = server_pb2.UpdateParamRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name;
        request.param.name = param_name
        if type(value) is int:
            request.param.value_int = value
        if type(value) is bool:
            request.param.value_bool = value
        if type(value) is float:
            request.param.value_float = value
        if type(value) is str:
            request.param.value_str = value

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.update_param(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with reload_filter : %s" % response.message)
                    else:
                        print("Error with reload_filter.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    ##########################################################################
    ############################### FILTER  ##################################
    ##########################################################################
    def reload_filter(self, filtre=None):
        """
            Reload Filter.
            Param : filtre - if None, reload all filter, else reload filter name
        """
        request = server_pb2.ReloadFilterRequest()
        if type(filtre) is list:
            for item in filtre:
                request.filterName.append(item)
        elif type(filtre) is str or type(filtre) is unicode:
            request.filterName.append(filtre)
        elif filtre is not None:
            raise Exception("filtre is wrong type : %s" % type(filtre))

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.reload_filter(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with reload_filter : %s" % response.message)
                    else:
                        print("Error with reload_filter.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_filter_list(self):
        """
            Return list of filter
        """
        request = server_pb2.GetFilterListRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filter_list(request, timeout=10000)
            returnValue = response.filters

        except Exception as ex:
            log.exception(ex)

        return returnValue

class Observer(threading.Thread):
    def __init__(self, observer, hostname, port):
        threading.Thread.__init__(self)
        self.observer = observer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.add = (hostname, port)
        self.close = False
        self.buffer = 65507

    def run(self):
        if self.observer:
            self.socket.sendto("I can see you.", self.add)
            while not self.close:
                sData = ""
                try:
                    data = self.socket.recv(self.buffer)
                    if data[0] != "b":
                        print("wrong type index.")
                        continue

                    i = 1
                    while i < self.buffer and data[i] != "_":
                        i += 1

                    nb_packet_string = data[1:i]
                    if nb_packet_string.isdigit():
                        nb_packet = int(nb_packet_string)
                    else:
                        print("wrong index.")
                        continue

                    sData += data[i + 1:]
                    for packet in range(1, nb_packet):
                        data, _ = self.socket.recvfrom(self.buffer)  # 262144 # 8192
                        if data[0] != "c":
                            print("wrong type index continue")
                            continue

                        i = 1
                        while i < self.buffer and data[i] != "_":
                            i += 1

                        no_packet_string = data[1:i]
                        if no_packet_string.isdigit():
                            no_packet = int(no_packet_string)
                            if no_packet != packet:
                                print("Wrong no packet : %d" % packet)
                        else:
                            print("wrong index continue.")
                            continue

                        sData += data[i + 1:]

                    self.observer(np.loads(sData))
                except Exception as e:
                    if not self.close:
                        print("Error udp observer : %s" % e)
        else:
            print("Error, self.observer is None.")

    def stop(self):
        self.close = True
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.socket.close()
            self.socket = None
        print("Close client")
