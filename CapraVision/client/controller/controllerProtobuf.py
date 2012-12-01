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

# Configure logging
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# The callback is for asynchronous call to RpcService
def callback(request, response):
    """Define a simple async callback."""
    log.info('Asynchronous response :' + response.__str__())

class Controller():
    def __init__(self):
        # Server details
        hostname = 'localhost'
        port = 8090

        # Create a new service instance
        self.service = RpcService(server_pb2.CommandService_Stub, port, hostname)

    def get_source(self):
        pass

    def get_chain(self):
        pass

    def get_thread(self):
        pass

    def change_sleep_time(self, sleep_time):
        pass

    def start_thread(self):
        pass

    def stop_thread(self):
        pass

    def __getitem__(self, index):
        pass

    def get_filter_from_index(self, index):
        pass

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
    
    def get_filter_list_from_filterchain(self):
        """
            Return list of filter from filterchain
        """
        request = server_pb2.GetFilterListFromFilterChainRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filter_list_from_filterchain(request, timeout=10000)
            returnValue = response.filters

        except Exception, ex:
            log.exception(ex)

        return returnValue

    def count_filters(self):
        pass

    def create_new_chain(self):
        pass

    def hook_new_chain(self, new_chain):
        pass

    def chain_exists(self):
        pass

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
            else:
                returnValue = False

        except Exception, ex:
            log.exception(ex)

        return returnValue

    def save_chain(self, file_name):
        pass

    def change_source(self, new_source):
        pass

    def is_thread_running(self):
        pass

    def thread_observer(self, image):
        pass

    def add_filter(self, filtre):
        pass

    def remove_filter(self, filtre):
        pass

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
            returnValue = not response.status

        except Exception, ex:
            log.exception(ex)

        return returnValue

    def move_filter_up(self, filtre):
        pass

    def move_filter_down(self, filtre):
        pass

    def add_image_observer(self, observer):
        pass

    def remove_image_observer(self, observer):
        pass

    def add_filter_observer(self, observer):
        pass

    def remove_filter_observer(self, observer):
        pass

    def add_filter_output_observer(self, output):
        pass

    def remove_filter_output_observer(self, output):
        pass

    def add_thread_observer(self, observer):
        pass

    def remove_thread_observer(self, observer):
        pass

    def close_server(self):
        pass

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
    