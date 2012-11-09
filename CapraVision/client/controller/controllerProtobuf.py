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
    
    def getFilter(self):
        request = server_pb2.GetFilterListRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.GetFilterList(request, timeout=10000)
            returnValue = response.filters 
            
        except Exception, ex:
            log.exception(ex)
            
        return returnValue
    
    
    
    
    
    
