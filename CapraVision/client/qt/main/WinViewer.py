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

#from gi.repository import GObject

from CapraVision.client.qt.utils import *

#from CapraVision.server.core.filterchain import chain
#from server import sources

class WinViewer():
    """Show the source after being processed by the filter chain.
    The window receives a filter in its constructor.  
    This is the last executed filter on the source.
    """
    def __init__(self,filterchain):        
        self.ui = get_ui(self, 'sourcesListStore', 'filterChainListStore')
        self.filterchain = filterchain
        filterchain.add_filter_observer(self.updateFilters)
        filterchain.add_image_observer(self.updateImage)
        
    def updateFilters(self):
        self.ui.filterComboBox.clear()
        for filter in self.filterchain.filters:
            self.ui.filterComboBox.addItem(filter.__class__.__name__)
    
    def updateImage(self,image):
        pass
    
    def getImageSource(self):
        pass
        

   
    