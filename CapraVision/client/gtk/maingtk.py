#!/usr/bin/env python

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
Description : Open gtk 
Authors: Benoit Paquet
Date : October 2012
"""

from CapraVision.server.core.mainloop import MainLoop
from CapraVision.server.core.manager import VisionManager
from CapraVision.server.tcp_server import Server

def run():
    thread = MainLoop()
    server = Server()
    server.start("127.0.0.1", 5030)
    c = VisionManager(thread)
    c.add_filter_output_observer(server.send)

    from gi.repository import Gtk, GObject
    import CapraVision.client.gtk.main
    GObject.threads_init()
    w = CapraVision.client.gtk.main.WinFilterChain(c)
    w.window.show_all()
    Gtk.main()

    server.stop()
    thread.stop()
    
if __name__ == '__main__':
    # Project path is parent directory
    import os 
    parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.sys.path.insert(0, parentdir)
    run()
    
