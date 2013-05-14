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
Description : Implementation of cmd, command line of python
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

from SeaGoatVision.server.core.manager import Manager
from SeaGoatVision.client.controller.controllerProtobuf import ControllerProtobuf
# SOURCE of this code about the commande line : http://www.doughellmann.com/PyMOTW/cmd/
import cmd

# Configure logging
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class VCmd(cmd.Cmd):
    def __init__(self, local=False, host="localhost", port=8090, completekey='tab', stdin=None, stdout=None, quiet=False):
        cmd.Cmd.__init__(self, completekey=completekey, stdin=stdin, stdout=stdout)
        self.quiet = quiet
        if local:
            self.controller = Manager()
        else:
            # Protobuf
            self.controller = ControllerProtobuf(host, port, quiet=quiet)

        # Directly connected to the vision server
        # self.controller = Manager()

        if not self.controller.is_connected():
            print("Vision server is not accessible.")
            return None

        if self.quiet:
            self.prompt = ""

    ##########################################################################
    # List of command
    ##########################################################################
    def do_is_connected(self, line):
        if not self.quiet:
            if self.controller.is_connected():
                print("You are connected.")
            else:
                print("You are disconnected.")

    def do_get_filter_list(self, line):
        lstFilter = self.controller.get_filter_list()
        if lstFilter is not None:
            print("Nombre de ligne %s, tableau : %s" % (len(lstFilter), lstFilter))
        else:
            print("No filterlist")

    def do_get_filterchain_list(self, line):
        lstFilterChain = self.controller.get_filterchain_list()
        lst_name = [item.name for item in lstFilterChain]
        if not self.quiet:
            if lstFilterChain is not None:
                print("Nombre de ligne %s, tableau : %s" % (len(lstFilterChain), lst_name))
            else:
                print("No lstFilterChain")
        else:
             print(lst_name)

    def do_add_output_observer(self, line):
        # execution_name
        param = line.split()
        self.controller.add_output_observer(param[0])

    def do_stop_output_observer(self, line):
        # execution_name
        param = line.split()
        self.controller.remove_output_observer(param[0])

    def do_start_filterchain_execution(self, line):
        # execution_name, media_name, filterchain_name
        param = line.split()
        self.controller.start_filterchain_execution(param[0], param[1], param[2])

    def do_stop_filterchain_execution(self, line):
        # execution_name
        param = line.split()
        self.controller.stop_filterchain_execution(param[0])

    def do_start_record(self, line):
        # media_name
        param = line.split()
        path = None
        if len(param) > 1:
            path = param[1]
        self.controller.start_record(param[0], path=path)

    def do_stop_record(self, line):
        # media_name
        param = line.split()
        self.controller.stop_record(param[0])

    def do_get_media_list(self, line):
        lst_media = self.controller.get_media_list()
        if not self.quiet:
            if lst_media is not None:
                print("Media list : %s" % lst_media)
            else:
                print("No media")
        else:
            print(lst_media)

    def do_EOF(self, line):
        # Redo last command
        return True
