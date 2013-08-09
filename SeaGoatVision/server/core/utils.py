#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
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

"""Contains not classable function"""
import os
import sys

def isnumeric(string):
    # TODO in python3, use str.isnumeric()
    try:
        float(string)
        return True
    except ValueError:
        return False

def add_filter_module(module, file):
    # param :
    # module like sys.modules[__name__]
    # file is __file__ from __init__.py
    for f in os.listdir(os.path.dirname(__file__)):
        if f.endswith(".py") and "__init__" not in f:
            filename, _ = os.path.splitext(f)
            mod = __import__('filters.public', fromlist=["facedetect"])
            pass
