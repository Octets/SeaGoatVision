#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
#
# SeaGoatVision is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons.shared_param import SharedParam
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class PoolParam(object):
    """
        This is common code to PoolPublicParam and PoolSharedParam.
    """

    def __init__(self):
        self._dct_param = None
        self._dct_param_manual = {}
        self._dct_shared_param = None
        self._dct_shared_param_manual = {}
        self._publisher = None
        self._cb_publish = None

    def destroy_param(self):
        for param in self._dct_param.values():
            param.destroy()
        for param in self._dct_param_manual.values():
            param.destroy()
        for param in self._dct_shared_param.values():
            param.destroy()
        for param in self._dct_shared_param_manual.values():
            param.destroy()

    # Get
    def get_params(self, param_name=None):
        if self._dct_param is None:
            self.sync_params()
        if param_name:
            if type(param_name) is list:
                return [self._dct_param.get(param_name) for param_name in
                        param_name]
            return self._dct_param.get(param_name)
        return self._dct_param

    def get_lst_params(self, param_name=None):
        if self._dct_param is None:
            self.sync_params()
        if not param_name:
            return []
        if type(param_name) is list:
            return [self._dct_param.get(param_name) for param_name in
                    param_name]
        return [self._dct_param.get(param_name)]

    def get_shared_params(self, param_name=None):
        if self._dct_shared_param is None:
            self.sync_params()
        if param_name:
            return self._dct_shared_param.get(param_name)
        return self._dct_shared_param

    def sync_params(self):
        dct_param = {}
        dct_shared_param = {}
        for name in dir(self):
            var = getattr(self, name)
            if isinstance(var, Param):
                name = var.get_name()
                dct_param[name] = var
                var.add_notify(self._add_notification_param)
            elif isinstance(var, SharedParam):
                name = var.get_name()
                dct_shared_param[name] = var
                var.add_notify(self._add_notification_param)
        # add manual param
        for name, param in self._dct_param_manual.items():
            dct_param[name] = param
            param.add_notify(self._add_notification_param)
        for name, param in self._dct_shared_param_manual.items():
            dct_shared_param[name] = param
            param.add_notify(self._add_notification_param)
        # copy it on used dict
        self._dct_param = dct_param
        self._dct_shared_param = dct_shared_param

    # Add
    def add_param(self, param):
        if self._dct_param is None:
            self.sync_params()
        self._add_param(self._dct_param, self._dct_param_manual, param)
        # notify itself
        param.add_notify(self._add_notification_param)

    def add_shared_param(self, param):
        if self._dct_shared_param is None:
            self.sync_params()
        self._add_param(self._dct_shared_param, self._dct_shared_param_manual,
                        param)

    def _add_param(self, dct_param, dct_param_manual, param):
        name = param.get_name()
        if name in dct_param:
            log.print_function(
                logger.error, "This param is already in the list : %s", name)
            return False
        dct_param[name] = param
        dct_param_manual[name] = param
        return True

    def _add_notification_param(self, param):
        # inherit it in child class
        pass

    # configuration
    def serialize(self, is_config=False):
        lst_serialize = []
        for name, param in self.get_params().items():
            lst_serialize.append(param.serialize(is_config=is_config))
        return lst_serialize

    def deserialize(self, data):
        if not data:
            return False
        if type(data) is dict:
            dct_params = data
        elif type(data) is list:
            dct_params = {param['name']: param for param in data}
        else:
            msg = "Wrong format data, suppose to be list in " \
                  "%s" % self.get_name()
            log.print_function(logger.error, msg)
            return False
        # search param in config
        status = True
        for name, param in self.get_params().items():
            dct_param = dct_params.get(name)
            if dct_param:
                status &= param.deserialize(dct_param)
        return status
