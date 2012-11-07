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
Description : Start the Vision Server
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

# Project path is parent directory
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

# Import required RPC modules
import protobuf.socketrpc.server as server
from vServer import vServerServiceImpl as impl

# Create and register the service
# Note that this is an instantiation of the implementation class,
# *not* the class defined in the proto file.
vserver_service = impl.VServerImpl()
server = server.SocketRpcServer(8090)
server.registerService(vserver_service)

# Start the server
print 'Serving on port 8090'
server.run()
