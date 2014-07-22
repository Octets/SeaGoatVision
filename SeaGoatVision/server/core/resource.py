#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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
import inspect

from SeaGoatVision.server.controller.publisher import Publisher
from configuration import Configuration
from SeaGoatVision.commons import keys
from SeaGoatVision.server.core import filterchain
from SeaGoatVision.server import media
from filter import Filter
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


class Resource(object):
    # TODO the resource.py need to manage execution access
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
            cls.dct_filter = {}

            # initialize subscriber server
            publisher = Publisher(5031)
            cls.publisher = publisher
            #self.resource.set_all_publisher(publisher)
            publisher.start()

            publisher.register(keys.get_key_execution_list())
            publisher.register(keys.get_key_filter_param())
            publisher.register(keys.get_key_media_param())
            publisher.register(keys.get_key_lst_rec_historic())

            # instance class
            cls._instance = super(Resource, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.dct_filter:
            self._load_filters()
        if not self.dct_media:
            self.load_media()

    # Utils
    def _module_name(self, name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    # Filterchain
    def get_filterchain_list(self):
        class FilterChain:
            def __init__(self):
                pass

        lst_filter_chain = []
        for fc_name in self.config.list_filterchain():
            lst_filter_chain.append({"name": fc_name, "doc": None})
        return lst_filter_chain

    def upload_filterchain(self, filterchain_name, s_contain):
        o_filterchain = filterchain.FilterChain(filterchain_name)
        status = o_filterchain.deserialize(filterchain_name, s_contain)
        if not status:
            return status
        return self.config.write_filterchain(o_filterchain)

    def delete_filterchain(self, filterchain_name):
        if filterchain_name in self.dct_filterchain:
            del self.dct_filterchain[filterchain_name]
        return self.config.delete_filterchain(filterchain_name)

    def get_filterchain(self, filterchain_name, force_new_filterchain=False):
        # check if already instance
        if not force_new_filterchain:
            o_filterchain = self.dct_filterchain.get(filterchain_name, None)
            if o_filterchain:
                return o_filterchain

        name = keys.get_empty_filterchain_name()
        if filterchain_name and filterchain_name != name:
            data = self.config.read_filterchain(filterchain_name)
            if not data:
                return
            o_filterchain = filterchain.FilterChain(
                filterchain_name, serialize=data)
        else:
            o_filterchain = filterchain.FilterChain(
                keys.get_empty_filterchain_name())

        self.dct_filterchain[filterchain_name] = o_filterchain
        return o_filterchain

    def get_filterchain_info(self, filterchain_name):
        o_filterchain = self.get_filterchain(filterchain_name)
        if o_filterchain is None:
            return {}
        return {"filters": o_filterchain.get_filter_list(),
                "default_media": o_filterchain.get_default_media_name()}

    def modify_filterchain(self, old_filterchain_name,
                           new_filterchain_name, lst_str_filters,
                           default_media):
        # create new filterchain
        if self.config.is_filterchain_exist(old_filterchain_name):
            active_old_filterchain = old_filterchain_name
        else:
            active_old_filterchain = None
        if self.create_filterchain(new_filterchain_name,
                                   lst_str_filters,
                                   default_media=default_media,
                                   old_configuration=active_old_filterchain):
            # delete old filterchain
            if old_filterchain_name != new_filterchain_name:
                return self.delete_filterchain(old_filterchain_name)
            return True
        # error with create filterchain
        return False

    def create_filterchain(
            self, filterchain_name, lst_str_filters, default_media=None,
            old_configuration=None):
        chain = filterchain.FilterChain(filterchain_name)
        index = 0
        for s_filter in lst_str_filters:
            if s_filter == keys.get_empty_filter_name():
                continue
            # Exception, remove the last -#
            pos = s_filter.rfind("-")
            if pos > 0:
                s_filter = s_filter[:pos]
            o_filter = self.create_filter(s_filter, index)
            index += 1
            if o_filter is None:
                # error, cancel the transaction
                return
            chain.add_filter(o_filter)

        chain.set_default_media_name(default_media)
        if old_configuration:
            old_chain_data = self.config.read_filterchain(old_configuration)
            if old_chain_data:
                if not chain.deserialize_update(filterchain_name,
                                                old_chain_data):
                    logger.warning("Cannot deserialize old configuration of \
                    filterchain %s." % filterchain_name)
            else:
                logger.warning("The filterchain %s is supposed to be in \
                memory if old exist." % filterchain_name)

        self.config.write_filterchain(chain)
        self.dct_filterchain[filterchain_name] = chain
        return chain

    # Filter
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
        import filters

        self.dct_filter = {name: filtre
                           for name, filtre in vars(filters).items()
                           if inspect.isclass(filtre)
                           if issubclass(filtre, Filter)
                           if "execute" in vars(filtre)}

    def reload_filter(self, filter_name):
        o_filter = self.dct_filter.get(filter_name, None)
        if not o_filter:
            log.print_function(
                logger.error,
                "The filter %s not exist in the list." %
                filter_name)
            return
        # reload the module
        if o_filter.__module__ == "SeaGoatVision.server.cpp.create_module":
            module = o_filter.__module_init__
        else:
            module = self._module_name(o_filter.__module__)
        reload(module)
        filter_class = getattr(module, filter_name)
        o_filter = filter_class()
        o_filter.set_name(filter_name)
        self.dct_filter[filter_name] = filter_class
        return o_filter

    def create_filter(self, filter_name, index):
        filter_class = self.get_filter_from_filter_name(filter_name)
        if not filter_class:
            return
        o_filter = filter_class()
        o_filter.set_name("%s-%d" % (filter_name, index))
        return o_filter

    def get_filter_from_filter_name(self, filter_name):
        return self.dct_filter.get(filter_name, None)

    # Media
    def load_media(self):
        # update list of media
        dct_media = {}
        # Create personalize media
        for conf_media in self.config.get_lst_media_config():
            name = conf_media.name
            o_media = conf_media.media(conf_media)
            if o_media.is_opened():
                if name in dct_media.keys():
                    log.print_function(
                        logger.error, "Media %s already exist." % name)
                    continue
                dct_media[name] = o_media
                logger.info("Media %s detected." % name)
            else:
                log.print_function(
                    logger.error, "Camera %s not detected" % name)
        # Force media_video
        media_video = media.media_video.MediaVideo(
            keys.get_media_file_video_name())
        dct_media[keys.get_media_file_video_name()] = media_video
        # TODO this is a hack to remove missing key warning about publisher
        # Register in publisher
        # media_video._get_cb_publisher()
        # Force create empty media
        from SeaGoatVision.server.media.implementation.empty import Empty

        dct_media[keys.get_media_empty_name()] = Empty(
            keys.get_media_empty_name())

        self.dct_media = dct_media
        self.set_all_publisher()

    def get_media_name_list(self):
        return self.dct_media.keys()

    def get_media(self, name):
        return self.dct_media.get(name, None)

    # Publisher
    def get_publisher(self):
        return self.publisher

    def set_all_publisher(self):
        publisher = self.publisher
        for media in self.dct_media.values():
            media.set_publisher(publisher)
