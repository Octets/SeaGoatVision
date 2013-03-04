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

from CapraVision.client.qt.utils import get_ui
from PySide import QtGui
from PySide import QtCore
from CapraVision.server.filters.implementation.python.bgr2rgb import BGR2RGB
from threading import Lock
import StringIO
import Image
import time

#from CapraVision.server.core.filterchain import chain
#from server import sources

class WinViewer(QtCore.QObject):
    """Show the source after being processed by the filter chain.
    The window receives a filter in its constructor.  
    This is the last executed filter on the source.    
    """
    
    newImage = QtCore.Signal(QtGui.QImage)
    
    def __init__(self,filterchain):  
        super(WinViewer, self).__init__()      
        self.ui = get_ui(self, 'sourcesListStore', 'filterChainListStore')
        self.filterchain = filterchain
        self.filter = filterchain.filters[len(filterchain.filters)-1]
        self.size = 1   
        self.lock = Lock()     
        
        filterchain.add_filter_observer(self.updateFilters)
        filterchain.add_image_observer(self.updateImage)        
           
        self.newImage.connect(self.setPixmap)
        self.ui.filterComboBox.currentIndexChanged.connect(self.changeFilter)
        self.ui.sizeComboBox.currentIndexChanged[str].connect(self.setImageScale)
        self.updateFilters()

        self.lastSecondFps = None
        self.fpsCount = 0
        
    def updateFilters(self):
        self.ui.filterComboBox.clear()
        for filter in self.filterchain.filters:
            self.ui.filterComboBox.addItem(filter.__class__.__name__)
    def changeFilter(self,index):
        self.filter = self.filterchain.filters[index]
    
    def updateImage(self,f,image):
        if f == self.filter:

            #fps
            iActualTime = time.time()
            if self.lastSecondFps is None:
                #Initiate fps
                self.lastSecondFps = iActualTime
                self.fpsCount = 1
            elif iActualTime - self.lastSecondFps > 1.0:
                self.ui.lbl_fps.setText("%d" % int(self.fpsCount))
                #new set
                self.lastSecondFps = iActualTime
                self.fpsCount = 1
            else:
                self.fpsCount += 1

            self.numpy_to_QImage(image)   
    
    def setPixmap(self,img):
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.imageLabel.setPixmap(pix)
    
    def numpy_to_QImage(self,image):
        bgr2rgb = BGR2RGB()
        imageRGB = bgr2rgb.execute(image)
        img = Image.fromarray(imageRGB)
        buff = StringIO.StringIO()
        img.save(buff, 'ppm')
        data = buff.getvalue()
        buff.close()        
        qimage = QtGui.QImage.fromData(data)
        if self.size <> 1.0:
            shape = image.shape
            qimage = qimage.scaled(shape[1]*self.size,shape[0]*self.size)          
        self.newImage.emit(qimage)
           
     
    def setImageScale(self,textSize):
        textSize = textSize[:-1]
        self.size = float(textSize)/100 
       
        

   
    