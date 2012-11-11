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

#from Server import filters
from PySide import QtGui
class WinFilter(QtGui.QDockWidget):
    def __init__(self,filter):
        super(WinFilter,self).__init__()
        self.filter=filter
        attr = getattr(filter, names)
        for att in attr:
            print att
            
        
    #def constructWidget(self,widget):
        
    
    
    
    
    
    
    
    
    