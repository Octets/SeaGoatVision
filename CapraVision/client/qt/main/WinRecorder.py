#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This filename is part of CapraVision.
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

from PySide import QtGui
from PySide import QtCore

from CapraVision.client.qt.utils import get_ui

class WinRecorder(QtCore.QObject):
    
    def __init__(self):
        super(WinRecorder, self).__init__()
        self.ui = get_ui(self)
    
        self.ui.playPauseButton.clicked.connect(self.playPauseButton_clicked)
        
    def playPauseButton_clicked(self):
        print 'allo'
    