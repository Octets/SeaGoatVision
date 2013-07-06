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
Description :
"""

from SeaGoatVision.server.tcp_server import Server
from configuration import Configuration
from resource import Resource
from SeaGoatVision.commons.keys import *
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

KEY_MEDIA = "media"
KEY_FILTERCHAIN = "filterchain"

class Manager:
    def __init__(self):
        """
            Structure of dct_execution
            {"execution_name" : {KEY_FILTERCHAIN : ref, KEY_MEDIA : ref}}
        """
        self.dct_exec = {}
        self.config = Configuration()
        self.resource = Resource()

        # tcp server for output observer
        self.server_observer = Server()
        self.server_observer.start("", 5030)
        self.notify_event_client = {}
        self.id_client_notify = 0

    def close(self):
        logger.info("Close manager and close server.")
        for execution in self.dct_exec.values():
            execution[KEY_MEDIA].close()
        self.server_observer.stop()

    ##########################################################################
    ################################ CLIENT ##################################
    ##########################################################################
    def is_connected(self):
        return True

    ##########################################################################
    ############################# SERVER STATE ###############################
    ##########################################################################
    def add_notify_server(self):
        self.id_client_notify += 1
        self.notify_event_client[self.id_client_notify] = False
        return self.id_client_notify

    def need_notify(self, id):
        notify = self.notify_event_client.get(id, None)
        if notify is None:
            logger.warning("The client id %s is not in the notify list.")
            return False
        if not notify:
            return False
        self.notify_event_client[id] = False
        return True

    def _active_notify(self):
        for notify in self.notify_event_client.keys():
            self.notify_event_client[notify] = True

    ##########################################################################
    ######################## EXECUTION FILTER ################################
    ##########################################################################
    def start_filterchain_execution(self, execution_name, media_name, filterchain_name, file_name=None):
        execution = self.dct_exec.get(execution_name, None)

        if execution:
            log.print_function(logger.error, "The execution %s is already created." % (execution_name))
            return False

        filterchain = self.resource.get_filterchain(filterchain_name, force_new_filterchain=True)
        if not filterchain:
            log.print_function(logger.error, "Filterchain %s not exist or contain error." % (filterchain_name))
            return False

        # Exception, if not media_name, we take the default media_name from the filterchain
        if not media_name:
            media_name = filterchain.get_default_media_name()

        media = self.resource.get_media(media_name)
        if not media:
            log.print_function(logger.error, "Media %s not exist or you didn't set the default media on filterchain." % (media_name))
            return False

        if media.is_media_video() and file_name:
            media.set_file(file_name)

        filterchain.set_media_param(media.get_dct_media_param())

        media.add_observer(filterchain.execute)

        self.dct_exec[execution_name] = {KEY_FILTERCHAIN: filterchain, KEY_MEDIA : media}

        self._active_notify()

        return True

    def stop_filterchain_execution(self, execution_name):
        execution = self.dct_exec.get(execution_name, None)

        if not execution:
            log.print_function(logger.warning, "The execution %s is already stopped." % execution_name)
            return False

        # Remove execution image observer from media
        observer = execution.get(KEY_MEDIA, None)
        if observer is None:
            logger.critical("Not found the observer about execution %s" % execution_name)
            return False
        filterchain = execution.get(KEY_FILTERCHAIN, None)
        if filterchain is None:
            logger.critical("Not found the filterchain about execution %s" % execution_name)
            return False

        observer.remove_observer(filterchain.execute)
        filterchain.destroy()
        del self.dct_exec[execution_name]
        self._active_notify()
        return True

    def get_execution_list(self):
        return self.dct_exec.keys()

    def get_execution_info(self, execution_name):
        exec_info = self.dct_exec.get(execution_name, None)
        if not exec_info:
            log.print_function(logger.error, "Cannot get execution info, it's empty.")
            return None
        class Exec_info: pass
        o_exec_info = Exec_info()
        setattr(o_exec_info, KEY_MEDIA, exec_info[KEY_MEDIA].get_name())
        setattr(o_exec_info, KEY_FILTERCHAIN, exec_info[KEY_FILTERCHAIN].get_name())
        return o_exec_info

    ##########################################################################
    ################################ MEDIA ###################################
    ##########################################################################
    def get_media_list(self):
        return {name: self.resource.get_media(name).get_type_media()
                for name in self.resource.get_media_name_list()}

    def cmd_to_media(self, media_name, cmd, value=None):
        media = self._get_media(media_name)
        if not media:
            return False
        if media.is_media_streaming():
            log.print_function(logger.error, "Cannot send a command to a streaming media %s." % media_name)
            return False
        return media.do_cmd(cmd, value)

    def get_info_media(self, media_name):
        media = self._get_media(media_name)
        if not media:
            return {}
        return media.get_info()

    def start_record(self, media_name, path=None):
        media = self._get_media(media_name)
        if not media:
            return False
        if media.is_media_video():
            log.print_function(logger.error, "Cannot start record to a media media %s." % media_name)
            return False
        return media.start_record(path=path)

    def stop_record(self, media_name):
        media = self._get_media(media_name)
        if not media:
            return False
        if media.is_media_video():
            log.print_function(logger.error, "Cannot stop record to a media media %s." % media_name)
            return False
        return media.stop_record()

    def get_params_media(self, media_name):
        media = self._get_media(media_name)
        if not media:
            return []
        return media.get_properties_param()

    def update_param_media(self, media_name, param_name, value):
        media = self._get_media(media_name)
        if not media:
            return False
        return media.update_property_param(param_name, value)

    def save_params_media(self, media_name):
        media = self._get_media(media_name)
        if not media:
            return False
        return self.config.write_media(media)

    ##########################################################################
    #############################  OBSERVER  #################################
    ##########################################################################
    def add_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name to select the filter
        """
        ret_value = False
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        return filterchain.add_image_observer(observer, filter_name)

    def set_image_observer(self, observer, execution_name, filter_name_old, filter_name_new):
        """
            Inform the server what filter we want to change observer
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name_old , filter to replace
                - string, filter_name_new , filter to use
        """
        if filter_name_old == filter_name_new:
            log.print_function(logger.error, "New and old filter_name is equal: %s" % filter_name_old)
            return False
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        filterchain.remove_image_observer(observer, filter_name_old)
        return filterchain.add_image_observer(observer, filter_name_new)

    def remove_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to remove observer
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name , filter to remove
        """
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        return filterchain.remove_image_observer(observer, filter_name)

    def add_output_observer(self, execution_name):
        """
            attach the output information of execution to tcp_server
            supported only one observer. Add observer to tcp_server
        """
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        if self.server_observer.send in filterchain.get_filter_output_observers():
            logger.warning("Manager: observer already exist - add_output_observer")
            return True
        return filterchain.add_filter_output_observer(self.server_observer.send)

    def remove_output_observer(self, execution_name):
        """
            remove the output information of execution to tcp_server
            supported only one observer. remove observer to tcp_server
        """
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        if not filterchain.get_filter_output_observers():
            return True
        return filterchain.remove_filter_output_observer(self.server_observer.send)

    ##########################################################################
    ########################## CONFIGURATION  ################################
    ##########################################################################

    ##########################################################################
    ############################ FILTERCHAIN  ################################
    ##########################################################################
    def reload_filter(self, filter_name=None):
        filter = self.resource.reload_filter(filter_name)
        if filter is None:
            return False
        for execution in self.dct_exec.values():
            filterchain = execution.get(KEY_FILTERCHAIN, None)
            if filterchain:
                filterchain.reload_filter(filter)
        return True

    def get_params_filterchain(self, execution_name, filter_name):
        # get actual filter from execution
        # TODO search information from configuration if execution not exist
        if not execution_name:
            return None
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return None
        return filterchain.get_params(filter_name=filter_name)

    def get_filterchain_info(self, filterchain_name):
        return self.resource.get_filterchain_info(filterchain_name)

    def update_param(self, execution_name, filter_name, param_name, value):
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        filter = filterchain.get_filter(name=filter_name)
        if not filter:
            log.print_function(logger.error, "Don't find filter %s on filterchain %s" % (filter_name, filterchain.get_name()))
            return False
        param = filter.get_params(param_name=param_name)
        if not param:
            log.print_function(logger.error, "Don't find param %s on filter %s" % (param_name, filter_name))
            return False

        param.set(value)
        filter.configure()
        return True

    def save_params(self, execution_name):
        "Force serialization and overwrite config"
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        return self.config.write_filterchain(filterchain)

    def get_filterchain_list(self):
        return self.resource.get_filterchain_list()

    def upload_filterchain(self, filterchain_name, s_file_contain):
        return self.resource.upload_filterchain(filterchain_name, s_file_contain)

    def delete_filterchain(self, filterchain_name):
        return self.resource.delete_filterchain(filterchain_name)

    def modify_filterchain(self, old_filterchain_name, new_filterchain_name, lst_str_filters, default_media):
        return self.resource.modify_filterchain(old_filterchain_name, new_filterchain_name, lst_str_filters, default_media)

    ##########################################################################
    ############################### FILTER  ##################################
    ##########################################################################
    def get_filter_list(self):
        return self.resource.get_filter_info_list()

    ##########################################################################
    ############################## PRIVATE  ##################################
    ##########################################################################
    def _get_filterchain(self, execution_name):
        dct_execution = self.dct_exec.get(execution_name, {})
        if not dct_execution:
            msg = "Don't find execution %s. List execution name: %s" % (execution_name, self.dct_exec.keys())
            log.print_function(logger.warning, msg, last_stack=True)
            return None
        filterchain = dct_execution.get(KEY_FILTERCHAIN, None)
        if not filterchain:
            msg = "Execution %s hasn't filterchain." % execution_name
            log.print_function(logger.critical, msg, last_stack=True)
            return None
        return filterchain

    def _get_media(self, media_name):
        media = self.resource.get_media(media_name)
        if not media:
            log.print_function(logger.error, "Cannot found the media %s." % media_name, last_stack=True)
            return None
        return media
