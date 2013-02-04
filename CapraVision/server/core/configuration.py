#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of CapraVision.
#
#    CapraVision is free software: you can redistribute it and/or modify
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

from CapraVision.server.filters import utils
import filterchain
import os

class Configuration:

    def __init__(self):
        self.dirFilterChain = "CapraVision/server/configuration/filterchain/"
        self.extFilterChain = ".filterchain"

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
        try:
            return os.remove(self._get_filename(filterchain_name))
        except OSError:
            return -1

    def get_filterchain(self, filterchain_name):
        return filterchain.read(self._get_filename(filterchain_name))

    def get_filters_from_filterchain(self, filterchain_name):
        o_filterchain = filterchain.read(self._get_filename(filterchain_name))
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
        dct_all_filters = utils.load_filters()
        chain = filterchain.FilterChain()
        for strFilter in lst_str_filters:
            filter = dct_all_filters.get(strFilter, None)
            if filter is None:
                # error, cancel the transaction
                return False
            chain.add_filter(filter())

        filterchain.write(self._get_filename(filterchain_name), chain)
        return True

    def _get_filename(self, filterchain_name):
        return self.dirFilterChain + filterchain_name + self.extFilterChain

