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

"""
Description : Start the Vision Server
"""

import os
import sys

from core.configuration import Configuration
from SeaGoatVision.commons import log
logger = log.get_logger(__name__)
config = Configuration()
path = config.get_log_file_path()
if path:
    log.add_handler(path)
# Import required RPC modules
from controller import jsonrpc_server


def run(p_port=None, verbose=False):
    global config
    config.set_verbose(verbose)
    # recheck if its locked because the last check is maybe a false lock
    pid = os.getpid()
    sFileLockName = "/tmp/SeaGoat.lock"
    if is_lock(sFileLockName):
        sys.exit(-1)

    fileLock = open(sFileLockName, "w")
    fileLock.write("%s" % pid)
    fileLock.close()

    if not p_port:
        port = config.get_tcp_output_config()
    else:
        port = p_port

    # Create and register the service
    server = jsonrpc_server.Jsonrpc_server(port)
    try:
        server.register()
    except Exception as e:
        log.printerror_stacktrace(logger, e)
        server.close()
        sys.exit(1)

    # Start the server
    logger.info('Serving on port %s - pid %s', port, pid)
    logger.info('Waiting command')
    try:
        server.run()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Close SeaGoat. See you later!")
    except Exception:
        raise(Exception)
    finally:
        server.close()
        # force closing the file
        os.remove(sFileLockName)


def is_lock(sFileLockName):
    # Create lock file
    # This technique counter the concurrence
    if os.path.isfile(sFileLockName):
        bIsLocked = True
    else:
        bIsLocked = False

    if bIsLocked:
        fileLock = open(sFileLockName, "r")
        pid = fileLock.readline()
        # check if this pid really exist
        if pid.isdigit():
            pid = int(pid)
            if check_pid(pid):
                logger.info(
                    "SeaGoat already run with the pid : %s - lock file %s",
                    pid,
                    sFileLockName)
                fileLock.close()
            else:
                # its a false lock
                bIsLocked = False
        else:
            logger.info(
                "SeaGoat lock is corrupted, see file : %s",
                sFileLockName)
    return bIsLocked


def check_pid(pid):
    """ Check For the existence of a pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
