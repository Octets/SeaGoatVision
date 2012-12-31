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
Description : Implementation of cmd, command line of python
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

from CapraVision.server.core.manager import Manager
from CapraVision.client.controller.controllerProtobuf import ControllerProtobuf
# SOURCE of this code about the commande line : http://www.doughellmann.com/PyMOTW/cmd/
import cmd

# Configure logging
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class VCmd(cmd.Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey=completekey, stdin=stdin, stdout=stdout)
        # Protobuf
        #self.controller = ControllerProtobuf()
    
        # Directly connected to the vision server
        self.controller = Manager()
        
        if not self.controller.is_connected():
            print("Vision server is not accessible.")
            return None
        
    ####################################################################################################
    # List of command
    ####################################################################################################
    def do_get_filter_list(self, line):
        lstFilter = self.controller.get_filter_list()
        if lstFilter is not None:
            print("Nombre de ligne %s, tableau : %s" % (len(lstFilter), lstFilter))
        else:
            print("No filterlist")
            
    def do_list_filterchain(self, line):
        lstFilterChain = self.controller.list_filterchain()
        if lstFilterChain is not None:
            print("Nombre de ligne %s, tableau : %s" % (len(lstFilterChain), lstFilterChain))
        else:
            print("No lstFilterChain")
            
    def do_EOF(self, line):
        # Redo last command
        return True

