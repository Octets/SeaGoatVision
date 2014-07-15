#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
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

import types
from PySide import QtGui
from PySide import QtCore
from SeaGoatVision.client.qt.utils import get_ui
from SeaGoatVision.client.qt.shared_info import SharedInfo
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class WinParamParent(QtGui.QDockWidget):
    # Use signal to update information from sub/pub
    # this fix crash with Qt threading.
    signal_update_param = QtCore.Signal(str)

    def __init__(self, controller, set_value):
        super(WinParamParent, self).__init__()
        self.signal_update_param.connect(self.update_param)

        self.shared_info = SharedInfo()

        self.controller = controller
        self.lst_param = None
        self._set_value = None
        self.layout = None
        self.ui = None
        self.lst_active_widget = []
        self.lst_inactive_widget = []
        self.parent_layout = None
        self.cb_group = None
        self.set_value = set_value

        self.reload_ui()

    def reload_ui(self):
        self.ui = get_ui(self, force_name="WinParam")

        self.lst_param = []
        self.clear_widget()

        self.cb_group = self.ui.cb_group
        self.parent_layout = self.ui.layout_params

        self.ui.saveButton.clicked.connect(self.save)
        self.ui.resetButton.clicked.connect(self.reset)
        self.ui.defaultButton.clicked.connect(self.default)
        self.ui.txt_search.returnPressed.connect(self.on_cb_group_item_changed)
        self.cb_group.currentIndexChanged.connect(
            self.on_cb_group_item_changed)

    def call_signal_param(self, json_data):
        self.signal_update_param.emit(json_data)

    def update_param(self, json_data):
        raise NotImplementedError("Need to implement update_param.")

    def update_server_param(self, param):
        param_name = param.get_name()
        # find if widget exist
        for widget in self.lst_active_widget:
            if widget.get_name() == param_name:
                widget.set_param_server(param)

    def update_module(self, is_empty, name, module_name, dct_description):
        # Ignore the not used param value
        self.clear_widget()
        if is_empty:
            self.ui.lbl_param_name.setText("Empty params")
            return

        if not self.lst_param:
            self.ui.lbl_param_name.setText("%s - Empty params" % name)
            return

        self.fill_group()
        self.on_cb_group_item_changed()

    def clear_widget(self):
        self.ui.txt_search.setText("")
        self.ui.cb_group.clear()
        self._hide_all_widget()

    def _set_widget(self, lst_param):
        self._hide_all_widget()
        if type(lst_param) is list:
            for param in lst_param:
                self._add_widget(param)
        elif isinstance(lst_param, Param):
            self._add_widget(lst_param)

    def _hide_all_widget(self):
        for i in reversed(range(len(self.lst_active_widget))):
            widget = self.lst_active_widget[i]
            widget.set_visible(False)
            self.lst_inactive_widget.append(widget)
            self.lst_active_widget.remove(widget)

    def _add_widget(self, param):
        # don't need to check for duplicate, it hide all widget each time
        # check in inactive list
        param_type = param.get_type()
        for widget in self.lst_inactive_widget:
            if widget.get_type() is param_type:
                self.lst_active_widget.append(widget)
                self.lst_inactive_widget.remove(widget)
                break
        else:
            widget = None
        # it's not exist, create a new one
        if not widget:
            if param_type is int:
                class_widget = IntWidget
            elif param_type is float:
                class_widget = FloatWidget
            elif param_type is str:
                class_widget = StrWidget
            elif param_type is bool:
                class_widget = BoolWidget
            elif param_type is types.NoneType:
                class_widget = NoneWidget
            else:
                logger.error("The type %s is not supported in WinParamParent "
                             "widget." % param_type)
                return
            widget = class_widget(self.controller, self.shared_info, param,
                                  self.parent_layout,
                                  self.set_value)
            self.lst_active_widget.append(widget)

        widget.set_param(param)
        widget.set_visible(True)
        return widget

    def fill_group(self):
        self.cb_group.clear()
        # get unique list of group
        lst_group = set(
            [group for param in self.lst_param for group in
             param.get_groups()])
        if lst_group:
            lst_group = list(lst_group)
            lst_group.sort()
            self.cb_group.addItem("")
            for group in lst_group:
                self.cb_group.addItem(group)

    def on_cb_group_item_changed(self, index=None):
        # apply filter
        text = self.ui.txt_search.text()
        if text:
            lst_param = [value for value in self.lst_param if
                         text in value.get_name()]
        else:
            lst_param = self.lst_param[:]
        # the first item of the group is empty
        group_name = self.cb_group.currentText()
        lst_param = self.get_lst_param_grouped(lst_param, group_name)
        self._set_widget(lst_param)

    @staticmethod
    def get_lst_param_grouped(lst_param, group):
        lst_param_sorted = sorted(lst_param,
                                  key=lambda x: x.get_name().lower())
        lst_param_grouped = []
        for param in lst_param_sorted:
            if not group or group in param.get_groups():
                lst_param_grouped.append(param)
        return lst_param_grouped


class ParentWidget(object):
    def __init__(self, controller, shared_info, param, parent_layout,
                 set_value):
        # The type of the widget cannot change
        # Manage only one parameter at time
        self.param_type = param.get_type()
        self.param = param
        self.parent_layout = parent_layout
        self.controller = controller
        self.shared_info = shared_info
        self.set_value = set_value
        self.is_visible = False
        self.lbl_desc = None
        self.group_box = None
        self._add_group_box()
        self.set_visible(False)

    def get_type(self):
        return self.param_type

    def get_name(self):
        return self.param.get_name()

    def _set_value(self, value):
        self.set_value(value, self.param)

    def set_visible(self, is_visible):
        self.group_box.setVisible(is_visible)
        self.is_visible = is_visible

    def _add_group_box(self):
        # call this just one time
        vertical_layout = QtGui.QVBoxLayout()
        # add layout on his parent
        layout = self._create_widget()
        # add description label
        self.lbl_desc = QtGui.QLabel()
        vertical_layout.addLayout(layout)
        vertical_layout.addWidget(self.lbl_desc)
        # create group_box
        self.group_box = QtGui.QGroupBox()
        self.group_box.setLayout(vertical_layout)
        self.parent_layout.addWidget(self.group_box)

    def set_param(self, param):
        # update param
        param_name = param.get_name()
        if param.get_type() is not self.param_type:
            logger.error(
                "Wrong param type receiving %s and expect %s" % (
                    param.get_type(), self.param_type))
            return

        is_lock = param.get_is_lock()
        self.group_box.setDisabled(is_lock)

        self.param = param
        self.lbl_desc.setText(param.get_description())
        self.group_box.setTitle(param_name)
        self._set_widget()

    def set_param_server(self, param):
        self._set_server_widget(param)

    def _create_widget(self):
        raise NotImplementedError("Need to implement _create_widget.")

    def _set_widget(self):
        raise NotImplementedError("Need to implement _set_widget.")

    def _set_server_widget(self):
        raise NotImplementedError("Need to implement _set_server_widget.")


class IntWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout,
                 set_value):
        self.slider = None
        self.spinbox = None
        self.lbl_server_value = None
        self.checkbox = None
        self.is_used_slider = False
        self._server_param = None
        super(self.__class__, self).__init__(controller, shared_info, param,
                                             parent_layout,
                                             set_value)

    def _create_widget(self):
        self.spinbox = spinbox = QtGui.QSpinBox()
        spinbox.setMaximumHeight(28)
        spinbox.setMaximumWidth(100)
        # TODO do we need to implement signal move up and down?
        spinbox.editingFinished.connect(self._spin_value_change)

        self.slider = slider = QtGui.QSlider()
        slider.setTickInterval(1)
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        slider.sliderMoved.connect(self._slider_value_change)
        slider.sliderPressed.connect(self._slider_press)
        slider.sliderReleased.connect(self._slider_release)

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
        self.lbl_server_value.setText(str(fake_value))

    def _slider_press(self):
        self.is_used_slider = True

    def _slider_release(self):
        self.is_used_slider = False
        if self._server_param:
            self._update_param_from_server(self._server_param)
            self._server_param = None

    def _set_server_widget(self, param):
        value = param.get()
        self.lbl_server_value.setText(str(value))
        if not self.is_used_slider:
            self._update_param_from_server(param)
        else:
            self._server_param = param

    def _update_param_from_server(self, param):
        self.param = param
        value = param.get()
        self.slider.setValue(value)
        self.spinbox.setValue(value)

    def _spin_value_change(self):
        if self.is_visible:
            value = self.spinbox.value()
            self.slider.setValue(value)
            self._set_value(value)

    def _slider_value_change(self, value):
        if self.is_visible:
            self.spinbox.setValue(value)
            self._set_value(value)


class FloatWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout,
                 set_value):
        self.slider = None
        self.spinbox = None
        self.lbl_server_value = None
        self.checkbox = None
        self.is_used_slider = False
        self._server_param = None
        self._new_slider_min = 0.0
        self._new_slider_max = 1.0
        super(self.__class__, self).__init__(controller, shared_info, param,
                                             parent_layout,
                                             set_value)

    def _create_widget(self):
        self.spinbox = spinbox = QtGui.QDoubleSpinBox()
        spinbox.setMaximumHeight(28)
        spinbox.setMaximumWidth(100)
        spinbox.editingFinished.connect(self._spin_value_change)

        self.slider = slider = QtGui.QSlider()
        slider.setTickInterval(1)
        slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        slider.sliderMoved.connect(self._slider_value_change)
        slider.sliderPressed.connect(self._slider_press)
        slider.sliderReleased.connect(self._slider_release)

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
        self.lbl_server_value.setText(str(fake_value))

    def _slider_press(self):
        self.is_used_slider = True

    def _slider_release(self):
        self.is_used_slider = False
        if self._server_param:
            self._update_param_from_server(self._server_param)
            self._server_param = None

    def _set_server_widget(self, param):
        value = param.get()
        self.lbl_server_value.setText(str(value))
        if not self.is_used_slider:
            self._update_param_from_server(param)
        else:
            self._server_param = param

    def _update_param_from_server(self, param):
        self.param = param
        value = param.get()
        self.slider.setValue(value)
        self.spinbox.setValue(value)

    def _spin_value_change(self):
        if self.is_visible:
            value = self.spinbox.value()
            self.slider.setValue(value)
            self._set_value(value)

    def _slider_value_change(self, value):
        if self.is_visible:
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
    def __init__(self, controller, shared_info, param, parent_layout,
                 set_value):
        # common widget
        self.line_edit = None
        self.combo_box = None
        super(self.__class__, self).__init__(controller, shared_info, param,
                                             parent_layout,
                                             set_value)

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
            if line_edit.text() == param.get():
                return
            line_edit.setText(str(param.get()))
        else:
            combo.setVisible(True)
            line_edit.setVisible(False)
            if combo.currentText() == param.get():
                return
            combo.clear()
            lst_value_sorted = sorted(lst_value)
            items = [str(v) for v in lst_value_sorted]
            items.sort()
            combo.addItems(items)
            combo.setCurrentIndex(lst_value_sorted.index(param.get()))

    def _set_server_widget(self, param):
        self.param = param
        lst_value = param.get_list_value()
        combo = self.combo_box
        line_edit = self.line_edit

        if not lst_value:
            combo.setVisible(False)
            line_edit.setVisible(True)
            line_edit.setText(str(param.get()))
        else:
            lst_value_sorted = sorted(lst_value)
            combo.setVisible(True)
            line_edit.setVisible(False)
            combo.currentIndexChanged.disconnect(self._signal_combo_change)
            combo.setCurrentIndex(lst_value_sorted.index(param.get()))
            combo.currentIndexChanged.connect(self._signal_combo_change)

    def _signal_combo_change(self, index):
        if self.is_visible and index >= 0:
            value = self.combo_box.currentText()
            self._set_value(value)

    def _signal_edit_line(self):
        if self.is_visible:
            value = self.line_edit.text()
            self._set_value(value)


class BoolWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout,
                 set_value):
        self.checkbox = None
        super(self.__class__, self).__init__(controller, shared_info, param,
                                             parent_layout,
                                             set_value)

    def _create_widget(self):
        self.checkbox = checkbox = QtGui.QCheckBox()
        checkbox.setTristate(False)
        checkbox.stateChanged.connect(self._signal_check_state)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(checkbox)
        return layout

    def _set_widget(self):
        param = self.param
        if param.get():
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)

    def _set_server_widget(self, param):
        self.param = param
        self._set_widget()

    def _signal_check_state(self, value):
        if self.is_visible:
            self._set_value(value)


class NoneWidget(ParentWidget):
    def __init__(self, controller, shared_info, param, parent_layout,
                 set_value):
        self.button = None
        super(self.__class__, self).__init__(controller, shared_info, param,
                                             parent_layout,
                                             set_value)

    def _create_widget(self):
        self.button = button = QtGui.QPushButton()
        button.clicked.connect(self._signal_clicked)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(button)
        return layout

    def _set_widget(self):
        param = self.param
        self.button.setText(param.get_name())

    def _set_server_widget(self, param):
        self.param = param
        self._set_widget()

    def _signal_clicked(self):
        if self.is_visible:
            self._set_value(None)
