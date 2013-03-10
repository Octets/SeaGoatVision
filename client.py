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
Description : launch vision client. Can choose multiple client
"""

import argparse

def runGtk():
    from CapraVision.client.gtk.maingtk import run
    run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Open client for vision server.')
    #parser.add_argument('string', metavar='interface name', type=str, default="gtk", help='cli, gtk or qt is supported.')
    parser.add_argument('interface', metavar='interface name', nargs='?', type=str, default="gtk", help='gtk is supported.')

    args = parser.parse_args()

    sInterface = args.interface.lower()
    if sInterface == "gtk":
        runGtk()
    else:
        print("Interface not supported : %s" % sInterface)
