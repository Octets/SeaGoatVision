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

from SeaGoatVision.commons import log
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import keys
import jsonrpclib
import numpy as np
import cv2
logger = log.get_logger(__name__)


class JsonClient():

    def __init__(self, port, host=""):
        self.rpc = jsonrpclib.Server('http://%s:%s' % (host, port))
        self._lst_port = []
        self._hostname = host
        # link observer viewer with deserialize observer
        self.dct_link_obs_des_obs = {}

    def __getattr__(self, name):
        return getattr(self.rpc, name)

    def close(self):
        # ignore it, else you "close" the remote server
        pass

    def set_subscriber(self, subscriber):
        self.subscriber = subscriber

    def add_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name to select the filter
        """
        status = self.rpc.add_image_observer(execution_name, filter_name)
        if status:
            key = keys.create_unique_exec_filter_name(execution_name, filter_name)
            des_observer = self._deserialize_image(observer)
            self.dct_link_obs_des_obs[observer] = des_observer
            status = self.subscriber.subscribe(key, des_observer)
        return status

    def set_image_observer(
            self, observer, execution_name, filter_name_old, filter_name_new):
        status = self.rpc.set_image_observer(execution_name, filter_name_old, filter_name_new)
        if status:
            new_key = keys.create_unique_exec_filter_name(execution_name, filter_name_new)
            old_key = keys.create_unique_exec_filter_name(execution_name, filter_name_old)
            des_observer = self.dct_link_obs_des_obs[observer]
            self.subscriber.desubscribe(old_key, des_observer)
            status = self.subscriber.subscribe(new_key, des_observer)
        return status

    def remove_image_observer(self, observer, execution_name, filter_name):
        status = self.rpc.remove_image_observer(execution_name, filter_name)
        key = keys.create_unique_exec_filter_name(execution_name, filter_name)
        des_observer = self.dct_link_obs_des_obs[observer]
        self.subscriber.desubscribe(key, des_observer)
        del self.dct_link_obs_des_obs[observer]
        return status

    def get_params_filterchain(self, execution_name, filter_name):
        lst_param_ser = self.rpc.get_params_filterchain(
            execution_name, filter_name)
        return self._deserialize_param(lst_param_ser)

    def get_params_media(self, media_name):
        lst_param_ser = self.rpc.get_params_media(media_name)
        return self._deserialize_param(lst_param_ser)

    def _deserialize_param(self, lst_param_ser):
        if lst_param_ser:
            return [Param("temp", None, serialize=param_ser) for param_ser in lst_param_ser]
        return []

    def _deserialize_image(self, cb):
        def deserialize_image(data):
            img = np.loads(data)
            img_cv = cv2.imdecode(img, 1)
            cb(img_cv)
        return deserialize_image
