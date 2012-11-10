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
Description : This is the facade to communicate with client and controller.
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

class FacadeClient():
    def __init__(self, sControlerName="protobuf"):
        self.controller = None
        
        # select good controller
        if sControlerName == "protobuf":
            from controllerProtobuf import Controller
        elif sControlerName == "sharedMemory":
            from controllerSharedMemory import Controller
        else:
            raise Exception("Don't find the controller %s" % (sControlerName))

        self.controller = Controller()
    
    def getFilter(self):
        return self.controller.getFilter()


