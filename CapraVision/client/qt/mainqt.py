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
import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

#import gui.filters.WinColorLevel

from PySide.QtGui import QApplication  
from PySide import QtCore
from PySide import QtUiTools

import qt.main
#import gui.sources
import sys

def run():
    app = QApplication(sys.argv)
    win = qt.main.WinMain()
    win.show()
    app.exec_()
    
if __name__ == '__main__':
    run()
    