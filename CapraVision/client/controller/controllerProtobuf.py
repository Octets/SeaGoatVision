#!/usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of CapraVision.
#
#    CapraVision is free software: you can redistribute it and/or modify
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
from protobuf.socketrpc import RpcService
from CapraVision.proto import server_pb2

import socket
import numpy as np
import threading

# Configure logging
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# The callback is for asynchronous call to RpcService
def callback(request, response):
    """Define a simple async callback."""
    log.info('Asynchronous response :' + response.__str__())

class ControllerProtobuf():
    def __init__(self):
        # Server details
        hostname = 'localhost'
        port = 8090

        # Create a new service instance
        self.service = RpcService(server_pb2.CommandService_Stub, port, hostname)
        
        self.observer = {}
        
        self.socket = None

    ##########################################################################
    ################################ CLIENT ##################################
    ##########################################################################
    def is_connected(self):
        print("Try connection")
        request = server_pb2.IsConnectedRequest()
        # Make an synchronous call
        response = None
        try:
            response = self.service.is_connected(request, timeout=10000) is not None
            if response:
                print("Connection sucessful")
        except Exception, ex:
            log.exception(ex)

        return response
    
    def close(self):
        """
            Close the socket connection.
        """
        print("Close connection.")
        
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

        observer = None
        
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

        except Exception, ex:
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
            

        except Exception, ex:
            log.exception(ex)

        return returnValue
        
    ##########################################################################
    ################################ SOURCE ##################################
    ##########################################################################
    def get_source_list(self):
        """
            Get the list for image provider.
        """
        request = server_pb2.GetSourceListRequest()
        # Make an synchronous call
        returnResponse = []
        try:
            response = self.service.get_source_list(request, timeout=10000)
            if response:
                returnResponse = response.source 
            else:
                print("No answer on get_source_list")
        except Exception, ex:
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
        
        local_observer = Observer(observer)
        local_observer.start()
        
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

        except Exception, ex:
            log.exception(ex)

        if not returnValue:
            local_observer.stop()
        else:
            self.observer[execution_name] = local_observer

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

        except Exception, ex:
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

        except Exception, ex:
            log.exception(ex)

        observer.stop()
        del self.observer[execution_name]

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

        except Exception, ex:
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

        except Exception, ex:
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
                        print("Error with start_filterchain_execution : %s" % response.message)
                    else:
                        print("Error with start_filterchain_execution.")
            else:
                returnValue = False
            

        except Exception, ex:
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


        except Exception, ex:
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
        for filter in lst_str_filters:
            request.lst_str_filters.add().name = filter
            
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


        except Exception, ex:
            log.exception(ex)

        return returnValue
        
    def load_chain(self, file_name):
        """
            load Filter.
            Param : file_name - path of filter to load into server
        """
        request = server_pb2.LoadChainRequest()
        request.filterName = file_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.load_chain(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with load_chain : %s" % response.message)
                    else:
                        print("Error with load_chain.")
            else:
                returnValue = False


        except Exception, ex:
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
        elif type(filtre) is str:
            request.filterName = [filtre]
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


        except Exception, ex:
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

        except Exception, ex:
            log.exception(ex)

        return returnValue

class Observer(threading.Thread):
    def __init__(self, observer):
        threading.Thread.__init__(self)
        self.observer = observer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", 5050))
    
    def run(self):
        if self.observer:
            while 1:
                data, address = self.socket.recvfrom(8192) # 262144
                sData = data
                for i in range(28):
                    data, address = self.socket.recvfrom(8192) # 262144
                    sData += data
                
                self.observer(np.loads(sData))
        else:
            print("Error, self.observer is None.")
            
    def stop(self):
        self.socket.close()



