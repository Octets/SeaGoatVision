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
Description : launch vision client. Can choose multiple client
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

import sys
import argparse

def runQt(local=False, host="localhost", port=8090):
    from CapraVision.client.qt.mainqt import run
    return run(local=local, host=host, port=port)

def runCli(local=False, host="localhost", port=8090):
    from CapraVision.client.cli.cli import run
    return run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Open client for vision server.')
    parser.add_argument('interface', metavar='interface name', nargs='?', type=str, default="qt", help='cli, gtk or qt is supported.')
    parser.add_argument('--local', action='store_true', help='Run server local, else remote.')
    parser.add_argument('--host', type=str, default="localhost", help='Ip adress of remote server.')
    parser.add_argument('--port', type=int, default=8090, help='Port of remote server.')

    args = parser.parse_args()

    sInterface = args.interface.lower()
    if sInterface == "qt":
        sys.exit(runQt(local=args.local, host=args.host, port=args.port))
    elif sInterface == "cli":
        sys.exit(runCli(local=args.local, host=args.host, port=args.port))
    else:
        print("Interface not supported : %s" % sInterface)

