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

class WinCamera(WinParamParent):
    def __init__(self, controller, subscriber):
        super(WinCamera, self).__init__(controller)
        self.subscriber = subscriber
        self.media_name = None
        self.shared_info.connect("media", self.set_camera)
        self.subscriber.subscribe(keys.get_key_media_param(), self.update_media_param)

    def reload_ui(self):
        super(WinCamera, self).reload_ui()
        self.set_camera()

    def set_camera(self, value=None):
        # Ignore the value
        self.ui.txt_search.setText("")
        self.dct_param = {}
        self.cb_param.currentIndexChanged.disconnect(self.on_cb_param_item_changed)
        self.cb_param.clear()
        self.cb_param.currentIndexChanged.connect(self.on_cb_param_item_changed)

        self.media_name = self.shared_info.get("media")
        self.clear_widget()
        if not self.media_name:
            self.ui.lbl_param_name.setText("Empty params")
            return

        self.lst_param = self.controller.get_params_media(self.media_name)
        if self.lst_param is None:
            self.lst_param = []

        if not self.lst_param:
            self.ui.lbl_param_name.setText("%s - Empty params" % self.media_name)
            self.clear_widget()
            return

        for param in self.lst_param:
            name = param.get_name()
            self.cb_param.addItem(name)
            self.dct_param[name] = param

        self.on_cb_param_item_changed(0)

    def update_media_param(self, json_data):
        data = json.loads(json_data)
        media = data.get("media", None)
        param_ser = data.get("param", None)
        if not media and media != self.media_name:
            return
        param = Param("temp", None, serialize=param_ser)
        if self.actuel_widget:
            type = param.get_type()
            if type is int or type is float:
                self.actuel_widget.setValue(param.get())
            elif type is str:
                self.actuel_widget.setText(param.get())

    def on_cb_param_item_changed(self, index):
        self.ui.lbl_param_name.setText("%s" % (self.media_name))

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
                status = self.controller.update_param_media(self.media_name, param.get_name(), value)
                if status:
                    param.set(value)
                else:
                    logger.error("Change value %s of param %s." % (value, param.get_name()))
            return set

        self.cb_value_change = create_value_change(param)

        layout = getWidget[param.get_type()](param, self.cb_value_change)
        groupBox.setLayout(layout)

        return groupBox

    def default(self):
        pass

    def reset(self):
        for param in self.lst_param:
            param.reset()
            status = self.controller.update_param_media(self.media_name, param.get_name(), param.get())
        self.set_camera()

    def save(self):
        self.controller.save_params_media(self.media_name)
