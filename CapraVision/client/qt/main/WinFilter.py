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


from PySide import QtGui
from PySide import QtCore
from CapraVision.server.filters.parameter import Parameter

class TempParameter:
    def __init__(self,parameter):
        self.parameter= parameter
        self.tempValue = parameter.get_current_value()

    def setTempValue(self,tempValue):
        self.tempValue = tempValue            
        
    def execute(self):
        self.parameter.set_current_value(self.tempValue)

class WinFilter(QtGui.QDockWidget):
    def __init__(self):
        super(WinFilter,self).__init__()
        self.setWidget(QtGui.QWidget())
        self.tempParameters = []
              
        
    def get_filter_attr(self,filter):
        widgetList = []
        for parameterName in dir(filter):
            parameter = getattr(filter, parameterName)
            if isinstance(parameter, Parameter):
                widgetList.append(self.getWidget(parameter))
        return widgetList
    
    def setFilter(self,filter):
        #self.clear()
        del self.tempParameters[:]
        self.widget().destroy()
        self.setWidget(QtGui.QWidget())
        self.filter=filter
        self.construct_widget(filter)             
            
        
    def construct_widget(self,filter):
        self.setWindowTitle(filter.__class__.__name__)
        layout = QtGui.QVBoxLayout()
        
        for widget in self.get_filter_attr(filter):
            layout.addWidget(widget)
            
        self.executeButton = QtGui.QPushButton()
        self.executeButton.clicked.connect(self.execute)
        self.executeButton.setText("Execute")
        layout.addWidget(self.executeButton)
       
        self.widget().setLayout(layout)
    
    def getWidget(self,parameter):
        groupBox = QtGui.QGroupBox()
        
        groupBox.setTitle(parameter.name)
        
        getWidget = {
                  Parameter.INT : self.getIntegerWidget,
                  Parameter.FLOAT : self.getFloatWidget,
                  Parameter.EVEN : self.getEvenWidget,
                  Parameter.ODD : self.getOddWidget,
                  }
        
        
        
        layout = getWidget[parameter.type](parameter)       
        groupBox.setLayout(layout)
        
        return groupBox
    
    def getIntegerWidget(self,parameter):
        tempParameter = TempParameter(parameter)
        self.tempParameters.append(tempParameter)
        
        numberLabel = QtGui.QLabel()
        numberLabel.setNum(parameter.currentValue)
        
        slider = QtGui.QSlider()        
        slider.setBaseSize(100,100)
        slider.setMinimum(parameter.minValue)
        slider.setMaximum(parameter.maxValue)
        slider.setTickInterval(1)
        slider.setValue(parameter.currentValue)
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        
        slider.valueChanged.connect(numberLabel.setNum)
        slider.valueChanged.connect(tempParameter.setTempValue)
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(numberLabel)
        return layout
    
    def getFloatWidget(self,parameter):
        print "float"
    
    def getEvenWidget(self,parameter):
        print "even"
    
    def getOddWidget(self,parameter):
        print "odd"
    
    def execute(self):
        for tempParameter in self.tempParameters:
            tempParameter.execute()
        if hasattr(self.filter, "configure"):
            self.filter.configure()
            print "conf"
    
    
    
    
    
    
    
    