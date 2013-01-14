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
Description : This is a wrapper of video observer 
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : January 2013
"""

import time
from CapraVision.proto import server_pb2
import numpy as np

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class ObserverSource():
    def __init__(self, service, execution_name):
        self.service = service
        self.execution_name = execution_name

    def next(self):
        """
            Get an image on an execution.
        """
        request = server_pb2.GetImageRequest()
        request.execution_name = self.execution_name
        # Make an synchronous call
        returnResponse = None
        try:
            aTime = time.time()
            response = self.service.get_image(request, timeout=10000)
            bTime = time.time()
            if response:
                returnResponse = np.loads(response.image)
            else:
                print("No answer on get_image")
            cTime = time.time()
            print("Send request time : %s, load time %s" % (bTime-aTime, cTime-bTime))
        except Exception, ex:
            log.exception(ex)

        return returnResponse
    
    def set_filter_name(self, sFilter):
        """
            Set a filter to observe
        """
        print("Ask to observer the filter %s on execution %s" % (sFilter, self.execution_name))
        request = server_pb2.SetImageFilterObserverRequest()
        request.execution_name = self.execution_name
        request.filter_name = sFilter
        
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.set_image_filter_observer(request, timeout=10000)
            if response:
               returnValue = not response.status
               if not returnValue:
                   if response.HasField("message"):
                       print("Error with set_filter_name : %s" % response.message)
                   else:
                       print("Error with set_filter_name.")
            else:
               returnValue = False
                
        except Exception, ex:
            log.exception(ex)

        return returnValue

    def stop(self):
        print("Stop observer")
    
