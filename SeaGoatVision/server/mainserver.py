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
# Import required RPC modules
import thirdparty.public.protobuf.socketrpc.server as server_rpc
from controller import protobufServerImpl as impl
from core.configuration import Configuration

def run(p_port=None):
    config = Configuration().get_config()
    # recheck if its locked because the last check is maybe a false lock
    pid = os.getpid()
    sFileLockName = "/tmp/SeaGoat.lock"
    if is_lock(sFileLockName):
        exit(-1)

    fileLock = open(sFileLockName, "w")
    fileLock.write("%s" % pid)
    fileLock.close()

    if not p_port:
        port = config.port_tcp_output
    else:
        port = p_port

    # Create and register the service
    # Note that this is an instantiation of the implementation class,
    # *not* the class defined in the proto file.
    server_service = impl.ProtobufServerImpl()
    server = server_rpc.SocketRpcServer(port, "")
    server.registerService(server_service)

    # Start the server
    print('Serving on port %s - pid %s' % (port, pid))
    print('Waiting command')
    try:
        server.run()
    except (KeyboardInterrupt, SystemExit):
        print("\nClose SeaGoat. See you later!")
    except Exception:
        raise(Exception)
    finally:
        server_service.close()
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
                print("SeaGoat already run with the pid : %s - lock file %s" % (pid, sFileLockName))
                fileLock.close()
            else:
                # its a false lock
                bIsLocked = False
        else:
            print("SeaGoat lock is corrupted, see file : %s" % sFileLockName)
    return bIsLocked

def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

