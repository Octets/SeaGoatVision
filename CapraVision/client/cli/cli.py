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
Description : Run the command line interface to communicate with the CapraVision Server
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""
import sys

def run():
    from vCmd import VCmd
    VCmd().cmdloop()
    return 0

if __name__ == '__main__':
    # Project path is parent directory
    import os 
    parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.sys.path.insert(0, parentdir)
    sys.exit(run())
