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
from WinParamParent import WinParamParent
from SeaGoatVision.commons import log
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import keys
import json

logger = log.get_logger(__name__)

class WinFilter(WinParamParent):
    def __init__(self, controller, subscriber):
        super(WinFilter, self).__init__(controller)
        self.subscriber = subscriber
        self.shared_info.connect("filter", self.set_filter)
        self.subscriber.subscribe(keys.get_key_filter_param(), self.update_filter_param)

    def set_filter(self, value=None):
        # Ignore the value
        self.ui.txt_search.setText("")
        self.dct_param = {}
        self.cb_param.currentIndexChanged.disconnect(self.on_cb_param_item_changed)
        self.cb_param.clear()
        self.cb_param.currentIndexChanged.connect(self.on_cb_param_item_changed)

        self.execution_name = self.shared_info.get("execution")
        self.filter_name = self.shared_info.get("filter")
        if not self.filter_name:
            self.clear_widget()
            self.ui.lbl_param_name.setText("Empty params")
            return

        self.lst_param = self.controller.get_params_filterchain(self.execution_name, self.filter_name)
        if self.lst_param is None:
            self.lst_param = []

        if not self.lst_param:
            self.ui.lbl_param_name.setText("%s - Empty params" % self.filter_name)
            self.clear_widget()
            return

        for param in self.lst_param:
            name = param.get_name()
            self.cb_param.addItem(name)
            self.dct_param[name] = param

        # Select first item
        self.on_cb_param_item_changed(0)

    def update_filter_param(self, json_data):
        data = json.loads(json_data)
        execution_name = data.get("execution_name", None)
        param_ser = data.get("param", None)
        if not execution_name and execution_name != self.execution_name:
            return
        param = Param("temp", None, serialize=param_ser)
        if self.actuel_widget:
            type = param.get_type()
            if type is int or type is float:
                self.actuel_widget.setValue(param.get())
            elif type is str:
                self.actuel_widget.setText(param.get())

    def on_cb_param_item_changed(self, index):
        self.ui.lbl_param_name.setText("%s - %s" % (self.execution_name, self.filter_name))

        self.clear_widget()

        if index == -1:
            return

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
                status = self.controller.update_param(self.execution_name, self.filter_name, param.get_name(), value)
                if status:
                    param.set(value)
                else:
                    logger.error("Change value %s of param %s." % (value, param.get_name()))
            return set

        cb_value_change = create_value_change(param)
        self.cb_value_change = cb_value_change

        layout = getWidget[param.get_type()](param, cb_value_change)
        groupBox.setLayout(layout)

        return groupBox

    def default(self):
        pass

    def reset(self):
        for param in self.lst_param:
            param.reset()
            status = self.controller.update_param(self.execution_name, self.filter_name, param.get_name(), param.get())
        self.set_filter()

    def save(self):
        self.controller.save_params(self.execution_name)
