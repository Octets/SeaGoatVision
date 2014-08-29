#! /usr/bin/env python2.7

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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
"""
Description : Run the vision server
"""
import argparse

import sys
argument = sys.argv[1:]
from SeaGoatVision.server.mainserver import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vision Server')
    parser.add_argument(
        "-p",
        '--port',
        type=int,
        default="0",
        help='port of the host')
    parser.add_argument(
        "-v",
        '--verbose',
        action="store_true",
        help="increase output verbosity")
    parser.add_argument(
        "-c",
        '--config',
        type=str,
        help="specify config file",
        default=None)
    args = parser.parse_args(args=argument)
    port = args.port if args.port else None
    run(p_port=port, verbose=args.verbose, config_path=args.config)
