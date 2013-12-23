#! /usr/bin/env python2.7

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

# This script compile filter in cpp.
# Be on root of project and call this script like this
# ./filters/build_cpp_filter.py

import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.append(parent_dir)

import filters
