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
import json

logger = log.get_logger(__name__)


class WinFilterParam(WinParamParent):
    def __init__(self, controller, subscriber):
        self.controller = controller
        self.dct_filter = self.controller.get_filter_list()
        super(WinFilterParam, self).__init__(controller, self.set_value)
        self.subscriber = subscriber
        self.shared_info.connect("filter", self.set_filter)
        # TODO Fill the exec name and filter name with cb shared info
        self.execution_name = None
        self.filter_name = None
        self.cb_param.currentIndexChanged.connect(self.on_cb_param_item_changed)
        self.subscriber.subscribe(keys.get_key_filter_param(), self.update_filter_param)

    def reload_ui(self):
        super(WinFilterParam, self).reload_ui()
        self.set_filter()
        self.ui.setWindowTitle('Filter param')

    def set_filter(self, value=None):
        self.filter_name = self.shared_info.get("filter")
        self.execution_name = self.shared_info.get("execution")
        is_empty = not self.filter_name

        if not is_empty:
            self.lst_param = self.controller.get_params_filterchain(self.execution_name,
                                                                    self.filter_name)
            if self.lst_param is None:
                self.lst_param = []

        self.update_module(is_empty, self.filter_name, "Filter", self.dct_filter)

    def update_filter_param(self, json_data):
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

    def on_cb_param_item_changed(self, index):
        module_name = "%s - %s" % (self.execution_name, self.filter_name)
        actual_param = self.lst_param[index]
        param = self.controller.get_param_filterchain(self.execution_name,
                                                      self.filter_name,
                                                      actual_param.get_name())
        super(WinFilterParam, self).on_cb_param_item_changed(index, module_name, param)

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
