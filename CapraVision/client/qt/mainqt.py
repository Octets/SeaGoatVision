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
Description : launch qt client 
Authors: Junior Gregoire (junior.gregoire@gmail.com)
Date : November 2012
"""
from PySide.QtGui import QApplication  

import main
import sys

from CapraVision.server.core.manager import Manager
#from CapraVision.server.tcp_server import Server
#from CapraVision.client.controller.controllerProtobuf import ControllerProtobuf


def run():
    # Protobuf
    #c = ControllerProtobuf()

    # Directly connected to the vision server
    c = Manager()
    
    if not c.is_connected():
        print("Vision server is not accessible.")
        return

    #server = Server()
    #server.start("127.0.0.1", 5030)
    
    app = QApplication(sys.argv)
    win = main.WinMain(c)
    win.show()
    rint = app.exec_()
    # close the server
    win.quit()
    c.close()
    
    return rint

    
if __name__ == '__main__':
    # Project path is parent directory
    import os 
    parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.sys.path.insert(0, parentdir)
    sys.exit(run())
    