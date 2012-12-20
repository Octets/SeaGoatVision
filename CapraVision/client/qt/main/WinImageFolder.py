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

from CapraVision.client.qt.utils import *
from CapraVision.server import filters

class WinImageImage:
    def __init__(self,imageFolder,folderPath=None):
        self.ui = get_ui(self)
        self.imageFolder = imageFolder
        self.folderPath = folderPath;
        
        if self.folderPath is not None:
            self.updateImageList()
        
    def updateImageList(self):
        pass
    
    def openNewFolder(self):
        pass
    
    def autoPlay(self):
        pass
    
    def nextImage(self):
        pass
    
    def firstImage(self):
        pass
    
    def previousImage(self):
        pass
    
    def lastImage(self):
        pass
    
    
    
    
