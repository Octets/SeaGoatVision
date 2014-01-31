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
from SeaGoatVision.client.qt.utils import get_ui
from SeaGoatVision.client.qt.shared_info import SharedInfo
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class WinParamParent(QtGui.QDockWidget):

    def __init__(self, controller):
        super(WinParamParent, self).__init__()
        self.shared_info = SharedInfo()

        self.controller = controller
        self.lst_param = None
        self.dct_param = None
        self.cb_value_change = None
        self.layout = None
        self.ui = None
        self._dct_widget_param = {}
        self.actual_dynamic_widget = None

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.lst_param = []
        self.dct_param = {}
        self.actual_dynamic_widget = None

        self.parent_layout = self.ui.layout_params
        self.cb_param = self.ui.cb_filter_param
        self.actuel_widget = None

        self.ui.saveButton.clicked.connect(self.save)
        self.ui.resetButton.clicked.connect(self.reset)
        self.ui.defaultButton.clicked.connect(self.default)
        self.ui.txt_search.returnPressed.connect(self._search_text_change)
        self.cb_param.currentIndexChanged.connect(
            self.on_cb_param_item_changed)

    def update_server_param(self, param):
        if self.actual_dynamic_widget:
            self.actual_dynamic_widget.set_param_server(param)

    def update_param(self, param):
        self._set_widget(param)

        self.ui.lbl_desc_param.setText(
            "Parameter description: %s" % (param.get_description()))

    def _search_text_change(self):
        # kk = {key: value for (key, value) in d.items() if s in key}
        text = self.ui.txt_search.text()
        if text:
            self.lst_param = [
                value for (
                    key,
                    value) in self.dct_param.items(
                    ) if text in key]
        else:
            self.lst_param = self.dct_param.values()
        self.cb_param.clear()
        for param in self.lst_param:
            name = param.get_name()
            self.cb_param.addItem(name)

    def _set_widget(self, param):
        param_type = param.get_type()
        dynamic_widget = self._dct_widget_param.get(param_type, None)
        if not dynamic_widget:
            dynamic_widget = self._DynamicWidget(param, self.parent_layout)
            self._dct_widget_param[param_type] = dynamic_widget
        if self.actual_dynamic_widget != dynamic_widget:
            # hide all widget
            for item in self._dct_widget_param.values():
                item.set_visible(False)
            dynamic_widget.set_visible(True)
        dynamic_widget.set_param(param)


    class _DynamicWidget():
        def __init__(self, controller, param, parent_layout):
            self.param_type = param.get_type()
            self.layout = None
            self.parent_layout = parent_layout
            layout = self._create_widget(param)
            self.parent_layout.addWidget(layout)
            self.controller = controller

        def get_layout(self):
            return self.layout

        def set_visible(self, is_visible):
            pass

        def set_param(self, param):
            print(param)

        def set_param_server(self, param):
            self.label.setText(str(param.get()))

        def _create_widget(self, param):
            group_box = QtGui.QGroupBox()

            group_box.setTitle(param.get_name())

            cb_value_change = self._create_value_change(param)
            self.cb_value_change = cb_value_change

            param_type = param.get_type()
            if param_type is int:
                layout = self._create_integer_widget(param, cb_value_change)
            elif param_type is float:
                layout = self._create_float_widget(param, cb_value_change)
            elif param_type is str:
                layout = self._create_str_widget(param, cb_value_change)
            elif param_type is bool:
                layout = self._create_bool_widget(param, cb_value_change)

            group_box.setLayout(layout)

            return group_box

        def _create_value_change(self, param):
            def _set_value(value):
                if param.get_type() is bool:
                    value = bool(value)
                status = self.controller.update_param(
                    self.execution_name,
                    self.filter_name,
                    param.get_name(),
                    value)
                if status:
                    param.set(value)
                else:
                    logger.error(
                        "Change value %s of param %s." %
                        (value, param.get_name()))
            return _set_value

        def _create_integer_widget(self, param, cb_value_change):
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

            self.label = label = QtGui.QLabel()
            label.setText("allo")

            value = param.get()
            if isinstance(value, tuple):
                spinbox.setValue(value[0])
                fake_value = value[0]
            else:
                spinbox.setValue(value)
                fake_value = value
            self._set_value = spinbox.setValue
            slider.setValue(fake_value)

            self.slider = slider
            slider.setTickPosition(QtGui.QSlider.TicksBothSides)
            slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

            spinbox.valueChanged.connect(self._spin_value_change)
            slider.valueChanged.connect(self._slider_value_change)

            layout = QtGui.QHBoxLayout()
            layout.addWidget(slider)
            layout.addWidget(spinbox)
            layout.addWidget(label)

            self.actuel_widget = spinbox
            return layout

        def _create_float_widget(self, param, cb_value_change):
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
            if isinstance(value, tuple):
                spinbox.setValue(value[0])
                fake_value = value[0]
            else:
                spinbox.setValue(value)
                fake_value = value
            self._set_value_float = spinbox.setValue
            slider.setValue(fake_value)

            slider.setTickPosition(QtGui.QSlider.TicksBothSides)
            slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

            layout = QtGui.QHBoxLayout()
            layout.addWidget(slider)
            layout.addWidget(spinbox)
            return layout

        def _fit(self, v, oldmin, oldmax, newmin=0.0, newmax=1.0):
            """
            Just a standard math fit/remap function

                number v         - initial value from old range
                number oldmin     - old range min value
                number oldmax     - old range max value
                number newmin     - new range min value
                number newmax     - new range max value

            Example:

                _fit(50, 0, 100, 0.0, 1.0)
                # 0.5

            """
            scale = (float(v) - oldmin) / (oldmax - oldmin)
            new_range = scale * (newmax - newmin)
            if newmin < newmax:
                return newmin + new_range
            else:
                return newmin - new_range

        def _float_slider_value_change(self, value):
            new_val = self._fit(
                value,
                self.slider_float.minimum(), self.slider_float.maximum(),
                self._new_slider_min, self._new_slider_max
            )
            if self._set_value_float:
                self._set_value_float(new_val)
            self.cb_value_change(new_val)

        def _float_spin_value_change(self, value):
            self.slider_float.setValue(value)
            self.cb_value_change(value)

        def _spin_value_change(self, value):
            self.slider.setValue(value)
            self.cb_value_change(value)

        def _slider_value_change(self, value):
            self._set_value(value)

        def _create_str_widget(self, param, cb_value_change):
            layout = QtGui.QHBoxLayout()
            lst_value = param.get_list_value()
            self.str_value_change = cb_value_change
            if not lst_value:
                self.line_edit = QtGui.QLineEdit()
                self.line_edit.setText(param.get())
                self.line_edit.returnPressed.connect(self._signal_edit_line)
                layout.addWidget(self.line_edit)
                self.actuel_widget = self.line_edit
            else:
                self.combo = QtGui.QComboBox()
                self.combo.addItems([str(v) for v in lst_value])
                layout.addWidget(self.combo)
                self.combo.setCurrentIndex(lst_value.index(param.get()))
                self.combo.currentIndexChanged.connect(self._signal_combo_change)

            return layout

        def _signal_combo_change(self, index):
            value = self.combo.currentText()
            self.str_value_change(value)

        def _signal_edit_line(self):
            value = self.line_edit.text()
            self.str_value_change(value)

        def _create_bool_widget(self, param, cb_value_change):
            checkbox = QtGui.QCheckBox()
            checkbox.setTristate(False)
            if param.get():
                checkbox.setCheckState(QtCore.Qt.Checked)
            checkbox.stateChanged.connect(cb_value_change)

            layout = QtGui.QHBoxLayout()
            layout.addWidget(checkbox)
            return layout
