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
"""
# SOURCE of this code about the commande line : http://www.doughellmann.com/PyMOTW/cmd/
import cmd
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

class VCmd(cmd.Cmd):
    def __init__(self, local=False, host="localhost", port=8090, completekey='tab', stdin=None, stdout=None, quiet=False):
        cmd.Cmd.__init__(self, completekey=completekey, stdin=stdin, stdout=stdout)
        self.quiet = quiet
        if local:
            from SeaGoatVision.server.core.manager import Manager
            self.controller = Manager()
        else:
            import jsonrpclib
            self.controller = jsonrpclib.Server('http://%s:%s' % (host, port))

        # Directly connected to the vision server
        # self.controller = Manager()

        if not self.controller.is_connected():
            logger.info("Vision server is not accessible.")
            return None

        if self.quiet:
            self.prompt = ""

    ##########################################################################
    # List of command
    ##########################################################################
    def do_is_connected(self, line):
        if not self.quiet:
            if self.controller.is_connected():
                logger.info("You are connected.")
            else:
                logger.info("You are disconnected.")

    def do_get_filter_list(self, line):
        lstFilter = self.controller.get_filter_list()
        if lstFilter is not None:
            logger.info("Nombre de ligne %s, tableau : %s" % (len(lstFilter), lstFilter))
        else:
            logger.info("No filterlist")

    def do_get_filterchain_list(self, line):
        lstFilterChain = self.controller.get_filterchain_list()
        lst_name = [item.name for item in lstFilterChain]
        if not self.quiet:
            if lstFilterChain is not None:
                logger.info("Nombre de ligne %s, tableau : %s" % (len(lstFilterChain), lst_name))
            else:
                logger.info("No lstFilterChain")
        else:
            logger.info(lst_name)

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
        name = ""
        if len(param):
            name = param[0]
        media = ""
        if len(param) > 1:
            media = param[1]
            if media == "None":
                media = ""
        filterchain = ""
        if len(param) > 2:
            filterchain = param[2]
            if filterchain == "None":
                filterchain = ""

        self.controller.start_filterchain_execution(name, media, filterchain)

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
                logger.info("Media list : %s" % lst_media)
            else:
                logger.info("No media")
        else:
            logger.info(lst_media)

    def do_EOF(self, line):
        # Redo last command
        return True
