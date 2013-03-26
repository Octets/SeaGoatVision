#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
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
from SeaGoatVision.commun.param import Param

class WinFilter(QtGui.QDockWidget):
    selectedFilterChanged = QtCore.Signal(object)

    def __init__(self, controller):
        super(WinFilter, self).__init__()
        self.setWidget(QtGui.QWidget())
        self.lst_param = []
        self.controller = controller

    def setFilter(self, execution_name, filter_name):
        # self.clear()
        del self.lst_param[:]
        self.widget().destroy()
        self.setWidget(QtGui.QWidget())
        self.filter_name = filter_name
        self.execution_name = execution_name
        self.construct_widget()

    def construct_widget(self):
        self.setWindowTitle(self.filter_name + " - " + self.execution_name)
        self.filter_param = self.controller.get_params_filterchain(self.execution_name, filter_name=self.filter_name)

        layout = QtGui.QVBoxLayout()

        if not self.filter_param:
            nothing = QtGui.QLabel()
            nothing.setText("Empty params.")
            layout.addWidget(nothing)
            self.widget().setLayout(layout)
            return

        for param in self.filter_param:
            layout.addWidget(self.getWidget(param))

        self.resetButton = QtGui.QPushButton()
        self.resetButton.clicked.connect(self.reset)
        self.resetButton.setText("Reset")
        layout.addWidget(self.resetButton)

        self.widget().setLayout(layout)

    def getWidget(self, param):
        groupBox = QtGui.QGroupBox()

        groupBox.setTitle(param.get_name())

        getWidget = {
            int : self.getIntegerWidget,
            float : self.getFloatWidget,
            str : self.getStrWidget,
            bool : self.getBoolWidget,
            }

        def create_value_change(param):
            def set(value):
                self.controller.update_param(self.execution_name, self.filter_name, param.get_name(), value)
            return set

        self.lst_param.append(param)
        layout = getWidget[param.get_type()](param, create_value_change(param))
        groupBox.setLayout(layout)

        return groupBox

    def getIntegerWidget(self, param, cb_value_change):
        numberLabel = QtGui.QLabel()
        value = param.get()
        if type(value) is tuple:
            numberLabel.setNum(value[0])
        else:
            numberLabel.setNum(value)

        slider = QtGui.QSlider()
        slider.setBaseSize(100, 100)
        slider.setMinimum(param.get_min())
        slider.setMaximum(param.get_max())
        slider.setTickInterval(1)
        if type(value) is tuple:
            slider.setValue(value[0])
        else:
            slider.setValue(value)
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        slider.valueChanged.connect(numberLabel.setNum)
        slider.valueChanged.connect(cb_value_change)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(numberLabel)
        return layout

    def getFloatWidget(self, param, cb_value_change):
        print "float"

    def getStrWidget(self, param, cb_value_change):
        print "string"

    def getBoolWidget(self, param, cb_value_change):
        boolLabel = QtGui.QLabel()
        boolLabel.setNum(param.get())

        checkbox = QtGui.QCheckBox()
        checkbox.stateChanged.connect(cb_value_change)
        if param.get():
            checkbox.setCheckState(QtCore.Qt.PartiallyChecked)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(checkbox)
        layout.addWidget(boolLabel)
        return layout

    def reset(self):
        for param in self.lst_param:
            param.reset()
