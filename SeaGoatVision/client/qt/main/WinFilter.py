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

# thanks for float_qslider.py : https://gist.github.com/justinfx/3427750

from PySide import QtGui
from PySide import QtCore
from SeaGoatVision.commons.param import Param
from SeaGoatVision.client.qt.utils import get_ui
from SeaGoatVision.client.qt.shared_info import Shared_info

class WinFilter(QtGui.QDockWidget):
    def __init__(self, controller):
        super(WinFilter, self).__init__()
        #self.setWidget(QtGui.QWidget())
        self.shared_info = Shared_info()

        self.controller = controller
        self.layout = None

        self.shared_info.connect("filter", self.setFilter)
        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.lst_param = []
        self.setValueFloat = None

        self.layout = self.ui.layout_params
        self.cb_param = self.ui.cb_filter_param

        self.ui.saveButton.clicked.connect(self.save)
        self.ui.resetButton.clicked.connect(self.reset)
        self.ui.defaultButton.clicked.connect(self.default)
        self.cb_param.currentIndexChanged.connect(self.on_cb_param_item_changed)

    def setFilter(self):
        execution_name = self.shared_info.get("execution")
        filter_name = self.shared_info.get("filter")
        self.filter_name = filter_name
        self.execution_name = execution_name
        if not self.filter_name:
            return

        self.lst_param = self.controller.get_params_filterchain(execution_name, filter_name=filter_name)
        self.cb_param.clear()
        for param in self.lst_param:
            self.cb_param.addItem(param.get_name())

        self.setWindowTitle("%s - %s" % (self.filter_name, self.execution_name))
        self.construct_widget()

    def construct_widget(self):
        if not self.lst_param:
            nothing = QtGui.QLabel()
            nothing.setText("Empty params.")
            self.layout.addWidget(nothing)
            return

        self.on_cb_param_item_changed(0)

    def on_cb_param_item_changed(self, index):
        if index == -1:
            return
        for i in range(self.layout.count()):
            b = self.layout.itemAt(i)
            b.widget().deleteLater()
        param = self.lst_param[index]
        self.layout.addWidget(self.getWidget(param))

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
                if param.get_type() is bool:
                    value = bool(value)
                self.controller.update_param(self.execution_name, self.filter_name, param.get_name(), value)
                param.set(value)
            return set

        cb_value_change = create_value_change(param)
        self.cb_value_change = cb_value_change

        layout = getWidget[param.get_type()](param, cb_value_change)
        groupBox.setLayout(layout)

        return groupBox

    def getIntegerWidget(self, param, cb_value_change):
        spinbox = QtGui.QSpinBox()
        spinbox.setMaximumHeight(28)
        spinbox.setMaximumWidth(100)

        slider = QtGui.QSlider()
        if param.get_min() is not None:
            slider.setMinimum(param.get_min())
            spinbox.setMinimum(param.get_min())
        if param.get_max() is not None:
            slider.setMaximum(param.get_max())
            spinbox.setMaximum(param.get_max())
        slider.setTickInterval(1)

        value = param.get()
        if type(value) is tuple:
            spinbox.setValue(value[0])
            fake_value = value[0]
        else:
            spinbox.setValue(value)
            fake_value = value
        self.setValue = spinbox.setValue
        slider.setValue(fake_value)

        self.slider = slider
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        spinbox.valueChanged.connect(self._spin_value_change)
        slider.valueChanged.connect(self._slider_value_change)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(spinbox)
        return layout

    def getFloatWidget(self, param, cb_value_change):
        spinbox = QtGui.QDoubleSpinBox()
        spinbox.setMaximumHeight(28)
        spinbox.setMaximumWidth(100)
        spinbox.valueChanged.connect(self._float_spin_value_change)

        slider = QtGui.QSlider()
        slider.valueChanged.connect(self._float_slider_value_change)
        self.slider_float = slider
        if param.get_min() is not None:
            slider.setMinimum(param.get_min())
            self._new_slider_min = param.get_min()
            spinbox.setMinimum(param.get_min())
        if param.get_max() is not None:
            slider.setMaximum(param.get_max())
            self._new_slider_max = param.get_max()
            spinbox.setMaximum(param.get_max())
        slider.setTickInterval(1)

        value = param.get()
        if type(value) is tuple:
            spinbox.setValue(value[0])
            fake_value = value[0]
        else:
            spinbox.setValue(value)
            fake_value = value
        self.setValueFloat = spinbox.setValue
        slider.setValue(fake_value)

        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(spinbox)
        return layout

    def fit(self, v, oldmin, oldmax, newmin=0.0, newmax=1.0):
        """
        Just a standard math fit/remap function

            number v         - initial value from old range
            number oldmin     - old range min value
            number oldmax     - old range max value
            number newmin     - new range min value
            number newmax     - new range max value

        Example:

            fit(50, 0, 100, 0.0, 1.0)
            # 0.5

        """
        scale = (float(v) - oldmin) / (oldmax - oldmin)
        new_range = scale * (newmax - newmin)
        if newmin < newmax:
            return newmin + new_range
        else:
            return newmin - new_range

    def _float_slider_value_change(self, value):
        newVal = self.fit(
            value,
            self.slider_float.minimum(), self.slider_float.maximum(),
            self._new_slider_min, self._new_slider_max
        )
        if self.setValueFloat:
            self.setValueFloat(newVal)
        self.cb_value_change(newVal)

    def _float_spin_value_change(self, value):
        self.slider_float.setValue(value)
        self.cb_value_change(value)

    def _spin_value_change(self, value):
        self.slider.setValue(value)
        self.cb_value_change(value)

    def _slider_value_change(self, value):
        self.setValue(value)

    def getStrWidget(self, param, cb_value_change):
        print "string"

    def getBoolWidget(self, param, cb_value_change):
        checkbox = QtGui.QCheckBox()
        checkbox.setTristate(False)
        if param.get():
            checkbox.setCheckState(QtCore.Qt.Checked)
        checkbox.stateChanged.connect(cb_value_change)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(checkbox)
        return layout

    def default(self):
        pass

    def reset(self):
        for param in self.lst_param:
            param.reset()
        self.setFilter()

    def save(self):
        self.controller.save_params(self.execution_name)
