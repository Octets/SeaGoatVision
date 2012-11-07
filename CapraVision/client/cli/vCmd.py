#! /usr/bin/env python

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
Description : Implementation of cmd, command line of python
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

# SOURCE of this code about the commande line : http://www.doughellmann.com/PyMOTW/cmd/
import cmd

# Import required RPC modules
from protobuf.socketrpc import RpcService
from vProto import vServer_pb2

# Configure logging
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# The callback is for asynchronous call to RpcService
def callback(request, response):
    """Define a simple async callback."""
    log.info('Asynchronous response :' + response.__str__())
    
class VCmd(cmd.Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey=completekey, stdin=stdin, stdout=stdout)
        
        # Server details
        hostname = 'localhost'
        port = 8090
        
        # Create a new service instance
        self.service = RpcService(vServer_pb2.CommandService_Stub, port, hostname)
    
    ####################################################################################################
    # List of command
    ####################################################################################################
    def do_getFilter(self, line):
        request = vServer_pb2.GetFilterListRequest()
        # Make an synchronous call
        try:
            log.info('Making synchronous call')
            response = self.service.GetFilterList(request, timeout=10000)
            log.info('Synchronous response: ' + response.__str__())
            
            print("Nombre de ligne %s, tableau : %s" % (len(response.filters), response.filters))
            
        except Exception, ex:
            log.exception(ex)
    
    def do_EOF(self, line):
        # Redo last command
        return True

