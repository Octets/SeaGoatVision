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

class ControllerProtobuf():
    def __init__(self):
        # Server details
        hostname = 'localhost'
        port = 8090

        # Create a new service instance
        self.service = RpcService(server_pb2.CommandService_Stub, port, hostname)

    def hello_world(self):
        print("Begin hello world")
        request = server_pb2.HelloWorldRequest()
        # Make an synchronous call
        response = None
        try:
            response = self.service.hello_world(request, timeout=10000) is not None
            if response:
                print("Recieve hello world :)")
            else:
                print("Wrong hello world :(")
        except Exception, ex:
            log.exception(ex)

        return response
    
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
    
    ##########################################################################
    ############################ FILTERCHAIN  ################################
    ##########################################################################
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


    ##########################################################################
    ############################### FILTER  ##################################
    ##########################################################################
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


    
