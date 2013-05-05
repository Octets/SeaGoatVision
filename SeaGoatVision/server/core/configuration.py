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

"""
Description : Configuration manage all configuration file.
Authors: Mathieu Benoit <mathben963@gmail.com>
Date : December 2012
"""

import os
import inspect
import types
import filters
from filter import Filter
import ConfigParser
from SeaGoatVision.commun.param import Param
from SeaGoatVision.commun.keys import *
from SeaGoatVision.server.core import filterchain
from SeaGoatVision.server.core import utils

class Configuration(object):
    def __init__(self):
        self.dirFilterChain = "SeaGoatVision/server/configuration/filterchain/"
        self.extFilterChain = ".filterchain"

        # {"filter_name" : class_filter }
        self.dct_filter = {}
        self.load_filters()
        self.dct_filterchain = {}

    #### Filterchain
    def get_filterchain_list(self):
        class FilterChain: pass
        lstFilterChain = []
        for files in os.listdir(self.dirFilterChain):
            if files.endswith(self.extFilterChain):
                filterChain = FilterChain()
                setattr(filterChain, "name", files[:-len(self.extFilterChain)])
                setattr(filterChain, "doc", None)
                lstFilterChain.append(filterChain)
        return lstFilterChain

    def upload_filterchain(self, filterchain_name, s_contain):
        f = open(self._get_filename(filterchain_name), "w")
        if f:
            f.write(s_contain)
            f.close()
            return True
        return False

    def delete_filterchain(self, filterchain_name):
        if filterchain_name in self.dct_filterchain:
            del self.dct_filterchain[filterchain_name]
        try:
            return os.remove(self._get_filename(filterchain_name))
        except OSError:
            return -1

    def get_filterchain(self, filterchain_name):
        # check if already instance
        o_filterchain = self.dct_filterchain.get(filterchain_name, None)
        if o_filterchain:
            return o_filterchain

        if filterchain_name and filterchain_name != get_empty_filterchain_name():
            o_filterchain = self.read_filterchain(self._get_filename(filterchain_name))
        else:
            o_filterchain = filterchain.FilterChain(get_empty_filterchain_name())
        self.dct_filterchain[filterchain_name] = o_filterchain
        return o_filterchain

    def get_filters_from_filterchain(self, filterchain_name):
        o_filterchain = self.get_filterchain(filterchain_name)
        return o_filterchain.get_filter_list()

    def modify_filterchain(self, old_filterchain_name, new_filterchain_name, lst_str_filters):
        # create new filterchain
        if self.create_filterchain(new_filterchain_name, lst_str_filters):
            # delete old filterchain
            if old_filterchain_name != new_filterchain_name:
                self.delete_filterchain(old_filterchain_name)
            return True
        # error with create filterchain
        return False

    def create_filterchain(self, filterchain_name, lst_str_filters):
        chain = filterchain.FilterChain(filterchain_name)
        for s_filter in lst_str_filters:
            o_filter = self.create_filter(s_filter)
            if o_filter is None:
                # error, cancel the transaction
                return False
            chain.add_filter(o_filter)

        self.write_filterchain(self._get_filename(filterchain_name), chain)
        return True

    def _get_filename(self, filterchain_name):
        return self.dirFilterChain + filterchain_name + self.extFilterChain

    def read_filterchain(self, file_name):
        """Open a filtre chain file and load its content in a new filtre chain."""
        filterchain_name = file_name[file_name.rfind("/") + 1:file_name.rfind(".")]
        new_chain = filterchain.FilterChain(filterchain_name)
        cfg = ConfigParser.ConfigParser()
        cfg.read(file_name)
        for section in cfg.sections():
            filtre = self.create_filter(section)
            if not filtre:
                print("Error : The filter %s doesn't exist on filterchain %s." % (section, filterchain_name))
                continue
            # TODO refaire les parameter seulement
            for member in filtre.__dict__:
                param = getattr(filtre, member)
                if not isinstance(param, Param):
                    continue
                try:
                    val = cfg.get(section, member)
                except:
                    # the file didn't contain the param
                    continue
                if val == "True" or val == "False":
                    param.set(cfg.getboolean(section, member))
                elif val.isdigit():
                    param.set(cfg.getint(section, member))
                elif utils.isnumeric(val):
                    f_value = cfg.getfloat(section, member)
                    # exception, if the param want int, we will cast it
                    if param.get_type() is int:
                        param.set(int(f_value))
                    else:
                        param.set(f_value)
                elif val[0] == "(":
                    # It's a tuple!
                    if val.find("."):
                        val = tuple(map(float, val[1:-1].split(',')))
                    else:
                        val = tuple(map(int, val[1:-1].split(',')))
                    param.set(val[0], thres_h=val[1])
                else:
                    val = '\n'.join([line[1:-1] for line in str.splitlines(val)])
                    param.set(val)
            if hasattr(filtre, 'configure'):
                filtre.configure()
            new_chain.add_filter(filtre)
        return new_chain

    def write_filterchain(self, file_name, chain):
        """Save the content of the filter chain in a file."""
        cfg = ConfigParser.ConfigParser()
        for fname, params in chain.get_params():
            cfg.add_section(fname)
            for param in params:
                value = param.get()
                name = param.get_name()
                if isinstance(value, str):
                    value = '\n'.join(['"%s"' % line for line in str.splitlines(value)])
                cfg.set(fname, name, value)
        cfg.write(open(file_name, 'w'))

    #### Filter
    def get_filter_name_list(self):
        return self.dct_filter.keys()

    def load_filters(self):
        # TODO : redo an import
        # TODO "class" key is important?
        # update list of filter
        self.dct_filter = {name: filtre
                        for name, filtre in vars(filters).items()
                        if inspect.isclass(filtre)
                        if issubclass(filtre, Filter)
                        if "execute" in vars(filtre)}

    def create_filter(self, filter_name):
        o_filter = self.get_filter_from_filterName(filter_name)
        if not o_filter:
            return None
        return o_filter()

    def get_filter_from_filterName(self, filter_name):
        return self.dct_filter.get(filter_name, None)
