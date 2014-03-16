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
Description : launch vision client. Can choose multiple client
"""

import sys
from SeaGoatVision.commons import global_env
import argparse
from SeaGoatVision.commons import log
from SeaGoatVision.client.controller.subscriber import Subscriber

logger = log.get_logger(__name__)


def run_qt(ctr, subscriber, local=False, host="localhost", port=8090):
    from SeaGoatVision.client.qt.mainqt import run
    return run(ctr, subscriber, local=local, host=host, port=port)


def run_cli(ctr, subscriber, local=False, host="localhost", port=8090, quiet=False):
    from SeaGoatVision.client.cli.cli import run
    return run(ctr, subscriber, local=local, host=host, port=port, quiet=quiet)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Open client for vision server.')
    parser.add_argument(
        'interface', metavar='interface name', nargs='?', type=str, default="qt",
        help='cli, gtk or qt is supported.')
    parser.add_argument(
        '--local',
        action='store_true',
        help='Run server local, else remote.')
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only print important information.')
    parser.add_argument(
        '--host',
        type=str,
        default="localhost",
        help='Ip adress of remote server.')
    parser.add_argument(
        '--port',
        type=int,
        default=8090,
        help='Port of remote server.')

    args = parser.parse_args()

    if args.local:
        global_env.set_is_local(True)
        from SeaGoatVision.server.core.cmdHandler import CmdHandler
        # Directly connected to the vision server
        ctr = CmdHandler()
    else:
        # Connect on remote with jsonrpc
        from SeaGoatVision.client.controller.json_client import JsonClient
        ctr = JsonClient(args.port, host=args.host)

    if not ctr.is_connected():
        logger.critical("Vision server is not accessible. Exit now.")
        ctr.close()
        sys.exit(-1)

    subscriber = Subscriber(ctr, 5031, addr=args.host)

    if not args.local:
        ctr.set_subscriber(subscriber)

    sInterface = args.interface.lower()
    if sInterface == "qt":
        sys.exit(
            run_qt(ctr, subscriber, local=args.local, host=args.host, port=args.port))
    elif sInterface == "cli":
        sys.exit(
            run_cli(ctr, subscriber, local=args.local, host=args.host, port=args.port, quiet=args.quiet))
    else:
        logger.error("Interface not supported : %s", sInterface)
