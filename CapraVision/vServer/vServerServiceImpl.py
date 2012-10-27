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
Description : Server Service implementation using vServer_pb2, generate by .proto file
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

# Import required RPC modules
from vProto import vServer_pb2

# Import CapraVision library
from CapraVision.filters import utils

class VServerImpl(vServer_pb2.CommandService):
    def __init__(self, *args, **kwargs):
        vServer_pb2.CommandService.__init__(self, *args, **kwargs)
    
    def GetFilterList(self, controller, request, done):
        print "Get Filter List"
        
        # Create a reply
        response = vServer_pb2.GetFilterListResponse()
        filters = utils.load_filters()
        for sFilter in filters.keys():
            response.filters.append(sFilter)
        
        print "Response : %s" % (response)
        
        # We're done, call the run method of the done callback
        done.run(response)
        
