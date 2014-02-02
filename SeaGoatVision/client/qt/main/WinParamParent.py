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
    def __init__(self, controller, set_value):
        super(WinParamParent, self).__init__()
        self.shared_info = SharedInfo()

        self.controller = controller
        self.lst_param = None
        self.dct_param = None
        self._set_value = None
        self.layout = None
        self.ui = None
        self._dct_widget_param = {}
        self.actual_dynamic_widget = None
        self.parent_layout = None
        self.cb_param = None
        self.set_value = set_value

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self)

        self.lst_param = []
        self.dct_param = {}
        self.actual_dynamic_widget = None

        self.parent_layout = self.ui.layout_params
        self.cb_param = self.ui.cb_filter_param

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
                    value) in self.dct_param.items() if text in key]
        else:
            self.lst_param = self.dct_param.values()
        self.cb_param.clear()
        for param in self.lst_param:
            name = param.get_name()
            self.cb_param.addItem(name)

    def clear_widget(self):
        for item in self._dct_widget_param.values():
            item.set_visible(False)
        self.ui.cb_filter_param.clear()

    def _set_widget(self, param):
        # TODO optimize double call set_widget
        param_type = param.get_type()
        dynamic_widget = self._dct_widget_param.get(param_type, None)
        if not dynamic_widget:
            if param_type is int:
                dynamic_widget = IntWidget(self.controller, self.shared_info, param, self.parent_layout, self.set_value)
            elif param_type is float:
                dynamic_widget = FloatWidget(self.controller, self.shared_info, param, self.parent_layout,
                                             self.set_value)
            elif param_type is str:
                dynamic_widget = StrWidget(self.controller, self.shared_info, param, self.parent_layout, self.set_value)
            elif param_type is bool:
                dynamic_widget = BoolWidget(self.controller, self.shared_info, param, self.parent_layout,
                                            self.set_value)
            self._dct_widget_param[param_type] = dynamic_widget
        if self.actual_dynamic_widget != dynamic_widget:
            # hide all widget
            for item in self._dct_widget_param.values():
                item.set_visible(False)
            dynamic_widget.set_visible(True)
        dynamic_widget.set_param(param)


class ParentWidget(object):
    def __init__(self, controller, shared_info, param, parent_layout, set_value):
        # The type of the widget cannot change
        # Manage only one parameter at time
        self.param_type = param.get_type()
        self.param = param
        self.parent_layout = parent_layout
        self.controller = controller
        self.shared_info = shared_info
        self.set_value = set_value
        # add layout on his parent
        layout = self._create_widget()
        self.group_box = QtGui.QGroupBox()
        self.group_box.setLayout(layout)
        if self.group_box:
            self.parent_layout.addWidget(self.group_box)
        else:
            raise Exception("Group_box of param widget is empty.")

    def _set_value(self, value):
        self.set_value(value, self.param)

    def set_visible(self, is_visible):
        if is_visible:
            self.group_box.setTitle(self.param.get_name())
        else:
            self.group_box.setTitle("")

    def set_param(self, param):
        # update param
        if param.get_type() is not self.param_type:
            logger.error("Wrong type receiving: %s" % param.get_type())
            return
        self.param = param
        self.group_box.setTitle(param.get_name())
        self._set_widget()

    def set_param_server(self, param):
        self._set_server_widget(param)

    def _create_widget(self):
        raise Exception("Need to implement _create_widget.")

    def _set_widget(self):
        raise Exception("Need to implement _set_widget.")

    def _set_server_widget(self):
        raise Exception("Need to implement _set_server_widget.")


class IntWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout, set_value):
        self.slider = None
        self.spinbox = None
        self.lbl_server_value = None
        self.checkbox = None
        super(self.__class__, self).__init__(controller, shared_info, param, parent_layout, set_value)

    def set_visible(self, is_visible):
        super(IntWidget, self).set_visible(is_visible)
        self.slider.setVisible(is_visible)
        self.spinbox.setVisible(is_visible)
        self.lbl_server_value.setVisible(is_visible)

    def _create_widget(self):
        self.spinbox = spinbox = QtGui.QSpinBox()
        spinbox.setMaximumHeight(28)
        spinbox.setMaximumWidth(100)
        spinbox.valueChanged.connect(self._spin_value_change)

        self.slider = slider = QtGui.QSlider()
        slider.setTickInterval(1)
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        slider.valueChanged.connect(self._slider_value_change)

        self.lbl_server_value = lbl_server = QtGui.QLabel()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(spinbox)
        layout.addWidget(lbl_server)
        return layout

    def _set_widget(self):
        param = self.param
        slider = self.slider
        spinbox = self.spinbox
        if param.get_min() is not None:
            slider.setMinimum(param.get_min())
            spinbox.setMinimum(param.get_min())
        if param.get_max() is not None:
            slider.setMaximum(param.get_max())
            spinbox.setMaximum(param.get_max())
        value = param.get()
        if isinstance(value, tuple):
            fake_value = value[0]
        else:
            fake_value = value
        spinbox.setValue(fake_value)
        slider.setValue(fake_value)

    def _set_server_widget(self, param):
        value = param.get()
        print(param)
        self.lbl_server_value.setText(str(value))

    def _spin_value_change(self, value):
        self.slider.setValue(value)
        self._set_value(value)

    def _slider_value_change(self, value):
        self.spinbox.setValue(value)
        self._set_value(value)


class FloatWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout, set_value):
        self.slider = None
        self.spinbox = None
        self.lbl_server_value = None
        self.checkbox = None
        self._new_slider_min = 0.0
        self._new_slider_max = 1.0
        super(self.__class__, self).__init__(controller, shared_info, param, parent_layout, set_value)

    def set_visible(self, is_visible):
        super(self.__class__, self).set_visible(is_visible)
        self.slider.setVisible(is_visible)
        self.spinbox.setVisible(is_visible)
        self.lbl_server_value.setVisible(is_visible)

    def _create_widget(self):
        self.spinbox = spinbox = QtGui.QDoubleSpinBox()
        spinbox.setMaximumHeight(28)
        spinbox.setMaximumWidth(100)
        spinbox.valueChanged.connect(self._spin_value_change)

        self.slider = slider = QtGui.QSlider()
        slider.setTickInterval(1)
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        slider.valueChanged.connect(self._slider_value_change)

        self.lbl_server_value = lbl_server = QtGui.QLabel()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(spinbox)
        layout.addWidget(lbl_server)
        return layout

    def _set_widget(self):
        param = self.param
        slider = self.slider
        spinbox = self.spinbox
        min_value = param.get_min()
        if min_value is not None:
            self._new_slider_min = param.get_min()
            slider.setMinimum(min_value)
            spinbox.setMinimum(min_value)
        max_value = param.get_max()
        if max_value is not None:
            self._new_slider_max = max_value
            slider.setMaximum(max_value)
            spinbox.setMaximum(max_value)
        value = param.get()
        if isinstance(value, tuple):
            fake_value = value[0]
        else:
            fake_value = value
        spinbox.setValue(fake_value)
        slider.setValue(fake_value)

    def _set_server_widget(self, param):
        value = param.get()
        self.lbl_server_value.setText(str(value))

    def _spin_value_change(self, value):
        self.slider.setValue(value)
        self._set_value(value)

    def _slider_value_change(self, value):
        new_val = self._fit(
            value,
            self.slider.minimum(), self.slider.maximum(),
            self._new_slider_min, self._new_slider_max
        )
        self.spinbox.setValue(new_val)
        self._set_value(new_val)

    @staticmethod
    def _fit(v, oldmin, oldmax, newmin=0.0, newmax=1.0):
        """
        Just a standard math fit/remap function
            number v          - initial value from old range
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


class StrWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout, set_value):
        # common widget
        self.line_edit = None
        self.combo_box = None
        super(self.__class__, self).__init__(controller, shared_info, param, parent_layout, set_value)

    def set_visible(self, is_visible):
        super(self.__class__, self).set_visible(is_visible)
        self.line_edit.setVisible(is_visible)
        self.combo_box.setVisible(is_visible)

    def _create_widget(self):
        layout = QtGui.QHBoxLayout()
        self.combo_box = combo = QtGui.QComboBox()
        combo.currentIndexChanged.connect(self._signal_combo_change)
        layout.addWidget(combo)

        self.line_edit = line_edit = QtGui.QLineEdit()
        self.line_edit.returnPressed.connect(self._signal_edit_line)
        layout.addWidget(line_edit)

        return layout

    def _set_widget(self):
        param = self.param
        lst_value = param.get_list_value()
        combo = self.combo_box
        line_edit = self.line_edit

        if not lst_value:
            combo.setVisible(False)
            line_edit.setVisible(True)
            line_edit.setText(param.get())
        else:
            combo.setVisible(True)
            line_edit.setVisible(False)
            combo.clear()
            combo.addItems([str(v) for v in lst_value])
            combo.setCurrentIndex(lst_value.index(param.get()))

    def _set_server_widget(self, param):
        value = param.get()
        self.lbl_server_value.setText(str(value))

    def _signal_combo_change(self, index):
        if index >= 0:
            value = self.combo_box.currentText()
            self._set_value(value)

    def _signal_edit_line(self):
        value = self.line_edit.text()
        self._set_value(value)


class BoolWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout, set_value):
        self.checkbox = None
        super(self.__class__, self).__init__(controller, shared_info, param, parent_layout, set_value)

    def set_visible(self, is_visible):
        super(self.__class__, self).set_visible(is_visible)
        self.checkbox.setVisible(is_visible)

    def _create_widget(self):
        self.checkbox = checkbox = QtGui.QCheckBox()
        checkbox.setTristate(False)
        checkbox.stateChanged.connect(self._set_value)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(checkbox)
        return layout

    def _set_widget(self):
        param = self.param
        if param.get():
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)

    def _set_server_widget(self):
        self._set_bool_widget()
