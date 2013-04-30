#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This filename is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
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
import os
import sys
import time
#from SeaGoatVision.server.core.utils import add_filter_module
from SeaGoatVision.server.cpp.create_module import *

# Global variable for cpp filter
# TODO find another solution to remove global variable, like log file
if 'cppfiles' not in globals():
    global cppfiles
    cppfiles = {}
if 'cpptimestamps' not in globals():
    global cpptimestamps
    cpptimestamps = {}

# add_filter_module(sys.modules[__name__], __file__)

# PYTHON FILTERS IMPORT
for f in os.listdir(os.path.dirname(__file__)):
    if not f.endswith(".py"):
        continue
    filename, _ = os.path.splitext(f)
    code = 'from %(module)s import *' % {'module' : filename}
    exec code

# C++ FILTERS IMPORT
import_all_cpp_filter(cppfiles, cpptimestamps, sys.modules[__name__], __file__)