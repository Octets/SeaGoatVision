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


class WinMediaParam(WinParamParent):
    def __init__(self, controller, subscriber):
        super(WinMediaParam, self).__init__(controller, self.set_value)
        self.subscriber = subscriber
        self.media_name = None
        self.shared_info.connect("media", self.set_camera)
        self.cb_param.currentIndexChanged.connect(self.on_cb_param_item_changed)
        self.subscriber.subscribe(keys.get_key_media_param(), self.update_media_param)

    def reload_ui(self):
        super(WinMediaParam, self).reload_ui()
        self.set_camera()
        self.ui.setWindowTitle('Media param')

    def set_camera(self, value=None):
        self.media_name = self.shared_info.get("media")
        is_empty = not self.media_name

        if not is_empty:
            self.lst_param = self.controller.get_params_media(self.media_name)
            if self.lst_param is None:
                self.lst_param = []

        #TODO implement description of params
        self.update_module(is_empty, self.media_name, "Media", None)

    def update_media_param(self, json_data):
        data = json.loads(json_data)
        media = data.get("media", None)
        param_ser = data.get("param", None)
        if not media and media != self.media_name:
            return
        param = Param("temp", None, serialize=param_ser)
        self.update_server_param(param)

    def on_cb_param_item_changed(self, index):
        module_name = "%s" % self.media_name
        actual_param = self.lst_param[index]
        param = self.controller.get_param_media(self.media_name, actual_param.get_name())
        super(WinMediaParam, self).on_cb_param_item_changed(index, module_name, param)

    def set_value(self, value, param):
        # update the server value
        if param is None:
            return
        param_name = param.get_name()
        param_type = param.get_type()
        if param_type is bool:
            value = bool(value)
        status = self.controller.update_param_media(self.media_name, param_name, value)
        if status:
            param.set(value)
        else:
            logger.error("Change value %s of param %s." % (value, param_name))

    def default(self):
        pass

    def reset(self):
        for param in self.lst_param:
            # TODO show status of the command
            param.reset()
            status = self.controller.update_param_media(
                self.media_name,
                param.get_name(),
                param.get())
        self.set_camera()

    def save(self):
        self.controller.save_params_media(self.media_name)
