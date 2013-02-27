#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This filename is part of CapraVision.
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
""" Filters implementations
    Rules:
        - Filter must be a class
        - Filter must have a execute(image) function that 
            returns the processed image
        - Filter can have a configure() function to configure the 
            object after creation
        - If there are data members that must not be saved, the member name
            must start with an underscore.  
            Eg: self._dont_save = 123 # value will not be save
                self.save = 456 # value will be saved"""

import os

for f in os.listdir(os.path.dirname(__file__)):
    if f.endswith(".pyc") or f.endswith(".py"):
        filename, _ = os.path.splitext(f)
        code = 'from %(module)s import *' % {'module' : filename}
        exec code
