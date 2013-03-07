#! /usr/bin/env python2.7

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
Description : Run the vision server
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""
import argparse

from CapraVision.server.mainserver import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vision Server')
    parser.add_argument('--port', type=int, default="8090", help='Port of the host.')
    args = parser.parse_args()
    run(port=args.port)

