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
Description : Manage the resource of the server: filters and media
"""
import os
import ConfigParser
import inspect

from configuration import Configuration
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons.keys import *
from SeaGoatVision.server.core import filterchain
from SeaGoatVision.server.core import utils
from SeaGoatVision.server import media
import filters
from filter import Filter

class Resource(object):
    _instance = None

    def __new__(cls):
        # Singleton
        if not cls._instance:
            # first instance
            cls.config = Configuration()
            cls.dct_filter = {}
            cls.dct_media = {}

            # {"filter_name" : class_filter}
            cls.dct_filterchain = {}

            # instance class
            cls._instance = super(Resource, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.dct_filter:
            self._load_filters()
        if not self.dct_media:
            self.load_media()

#### Filterchain
    def get_filterchain_list(self):
        class FilterChain: pass
        lstFilterChain = []
        for fc_name in self.config.list_filterchain():
                filterChain = FilterChain()
                setattr(filterChain, "name", fc_name)
                setattr(filterChain, "doc", None)
                lstFilterChain.append(filterChain)
        return lstFilterChain

    def upload_filterchain(self, filterchain_name, s_contain):
        return self.config.create_filterchain(filterchain_name, s_contain)

    def delete_filterchain(self, filterchain_name):
        if filterchain_name in self.dct_filterchain:
            del self.dct_filterchain[filterchain_name]
        self.config.delete_filterchain(filterchain_name)

    def get_filterchain(self, filterchain_name, force_new_filterchain=False):
        # check if already instance
        if not force_new_filterchain:
            o_filterchain = self.dct_filterchain.get(filterchain_name, None)
            if o_filterchain:
                return o_filterchain

        if filterchain_name and filterchain_name != get_empty_filterchain_name():
            data = self.config.read_filterchain(filterchain_name)
            if not data:
                return
            # Temporary name - empty
            o_filterchain = filterchain.FilterChain("System - Empty")
            o_filterchain.deserialize(filterchain_name, data, self.create_filter)
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

        self.config.write_filterchain(chain)
        self.dct_filterchain[filterchain_name] = chain
        return True

    #### Filter
    def get_filter_info_list(self):
        dct_info = {}
        for name in self.dct_filter.keys():
            doc = self.dct_filter[name].__doc__
            if doc is None:
                doc = ""
            dct_info[name] = doc
        return dct_info

    def _load_filters(self):
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

    #### Media
    def load_media(self):
        # update list of media
        dct_media = {}
        for name, media_class in vars(media).items():
            # only class can be a media
            if not inspect.isclass(media_class):
                continue
            # don't add first subclass, it's not a device
            if not(media_class is not media.media_video.Media_video and
                media_class is not media.media_streaming.Media_streaming):
                continue
            # add only subclass
            # ignore media.media_streaming.Media_streaming
            if issubclass(media_class, media.media_video.Media_video):
                dct_media[name] = media_class()
        # Create personalize media
        for conf_media in self.config.get_lst_media_config():
            name = conf_media.name
            if name in dct_media.keys():
                print("Error: media %s already exist." % name)
                continue
            o_media = conf_media.media(conf_media)
            if o_media.is_opened():
                dct_media[name] = o_media
            else:
                print("Error: Camera not detected %s" % name)
        self.dct_media = dct_media

    def get_media_name_list(self):
        return self.dct_media.keys()

    def get_media(self, name):
        return self.dct_media.get(name, None)

