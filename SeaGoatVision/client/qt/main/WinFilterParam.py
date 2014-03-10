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

from WinParamParent import WinParamParent
from SeaGoatVision.commons import log
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import keys
from SeaGoatVision.client.qt.shared_info import SharedInfo
from PySide import QtCore
import json

logger = log.get_logger(__name__)


class WinFilterParam(WinParamParent):
    def __init__(self, controller, subscriber):
        self.controller = controller
        self.dct_filter = self.controller.get_filter_list()
        super(WinFilterParam, self).__init__(controller, self.set_value)
        self.subscriber = subscriber
        self.shared_info.connect(SharedInfo.GLOBAL_FILTER, self.set_filter)
        self.shared_info.connect(SharedInfo.GLOBAL_CLOSE_EXEC, self.close_exec)
        self.shared_info.connect(SharedInfo.GLOBAL_RELOAD_FILTER, self.reload_filter)
        self.execution_name = None
        self.filter_name = None
        self.subscriber.subscribe(keys.get_key_filter_param(), self.call_signal_param)

    def reload_ui(self):
        super(WinFilterParam, self).reload_ui()
        self.set_filter()
        self.ui.setWindowTitle('Filter param')

    def reload_filter(self, filter_name):
        actual_filter_name = self.shared_info.get(SharedInfo.GLOBAL_FILTER)
        if not actual_filter_name:
            return
        # TODO add the real name and the fake name in filter to remove this check ("-")
        pos_key = actual_filter_name.rfind("-")
        key_name = actual_filter_name
        if pos_key > -1:
            key_name = key_name[:pos_key]
        if key_name == filter_name:
            # save last param name to refocus it
            text_group = self.cb_group.currentText()
            search_txt = self.ui.txt_search.text()
            self.set_filter()

            self.ui.txt_search.setText(search_txt)
            if text_group:
                # search index of group
                index_group = self.cb_group.findText(text_group, flags=QtCore.Qt.MatchExactly)
                if index_group == -1:
                    index_group = 0
                self.cb_group.setCurrentIndex(index_group)

    def set_filter(self, value=None):
        self.filter_name = self.shared_info.get(SharedInfo.GLOBAL_FILTER)
        exec_info = self.shared_info.get(SharedInfo.GLOBAL_EXEC)
        self.execution_name = None if not exec_info else exec_info[0]
        is_empty = not self.filter_name

        if not is_empty:
            self.lst_param = self.controller.get_params_filterchain(self.execution_name,
                                                                    self.filter_name)
            if self.lst_param is None:
                self.lst_param = []

        self.update_module(is_empty, self.filter_name, "Filter", self.dct_filter)

    def close_exec(self, exec_name):
        if self.execution_name != exec_name:
            return
        self.clear_widget()

    def update_param(self, json_data):
        data = json.loads(json_data)
        execution_name = data.get("execution", None)
        if not execution_name and execution_name != self.execution_name:
            return
        filter_name = data.get("filter", None)
        if not filter_name and filter_name != self.filter_name:
            return
        param_ser = data.get("param", None)
        if not param_ser:
            return
        param = Param("temp", None, serialize=param_ser)
        self.update_server_param(param)

    def set_value(self, value, param):
        # update the server value
        if param is None:
            return
        param_name = param.get_name()
        param_type = param.get_type()
        if param_type is bool:
            value = bool(value)
        status = self.controller.update_param(self.execution_name, self.filter_name, param_name,
                                              value)
        if status:
            param.set(value)
        else:
            logger.error("Change value %s of param %s." % (value, param_name))

    def default(self):
        pass

    def reset(self):
        for param in self.lst_param:
            param.reset()
            self.controller.update_param(self.execution_name, self.filter_name, param.get_name(),
                                         param.get())
        self.set_filter()

    def save(self):
        self.controller.save_params(self.execution_name)
