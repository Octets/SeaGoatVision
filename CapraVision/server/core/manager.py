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
Description :
Authors: Benoit Paquet
         Mathieu Benoit <mathben963@gmail.com>
Date : Novembre 2012
"""

from CapraVision.server.core.mainloop import MainLoop
from CapraVision.server import imageproviders
import filterchain
from CapraVision.server.filters import utils
from configuration import Configuration
import time
import numpy
from CapraVision.server.tcp_server import Server

class Manager:
    def __init__(self):
        """
            Structure of dct_thread
            {"execution_name" : {"thread" : ref, "filterchain" : ref}}
        """
        self.dct_thread = {}
        self.configuration = Configuration()
        
        # tcp server for output observer
        self.server_observer = Server()
        self.server_observer.start("", 5030)

    def close(self):
        print("Close manager")
        for thread in self.dct_thread.values():
            thread["thread"].quit()
        self.server_observer.stop()
    
    ##########################################################################
    ################################ CLIENT ##################################
    ##########################################################################
    def is_connected(self):
        return True
    
    ##########################################################################
    ############################# SERVER STATE ###############################
    ##########################################################################
    
    ##########################################################################
    ######################## EXECUTION FILTER ################################
    ##########################################################################
    def start_filterchain_execution(self, execution_name, source_name, filterchain_name):
        thread = self.dct_thread.get(execution_name, None)
        
        if thread:
            # change this, return the actual thread
            print("The execution %s is already created." % execution_name)
            return None
        
        source = imageproviders.load_sources().get(source_name, None)
        filterchain = self.configuration.get_filterchain(filterchain_name)

        if not(source and filterchain):
            print("Erreur with the source \"%s\" or the filterchain \"%s\". Maybe they dont exist." 
                  % (source, filterchain))
            return None
        
        source = source()
        
        thread = MainLoop()
        thread.add_observer(filterchain.execute)
        thread.start(source)
        
        self.dct_thread[execution_name] = {"thread" : thread, "filterchain" : filterchain}
        
        return True
    
    def stop_filterchain_execution(self, execution_name):
        thread = self.dct_thread.get(execution_name, None)
        
        if not thread:
            # change this, return the actual thread
            print("The execution %s is already stopped." % execution_name)
            return None
        
        thread["thread"].quit()
        del self.dct_thread[execution_name]
        
        return True
        
    ##########################################################################
    ################################ SOURCE ##################################
    ##########################################################################
    def get_source_list(self):
        return imageproviders.load_sources().keys()

    ##########################################################################
    ############################### THREAD  ##################################
    ##########################################################################
    
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
        dct_thread = self.dct_thread.get(execution_name, {})
        if dct_thread:
            filterchain = dct_thread.get("filterchain", None)
            if filterchain:
                ret_value = filterchain.add_image_observer(observer, filter_name)
        return ret_value
    
    def set_image_observer(self, observer, execution_name, filter_name_old, filter_name_new):
        """
            Inform the server what filter we want to change observer
            Param : 
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name_old , filter to replace
                - string, filter_name_new , filter to use
        """
        ret_value = False
        if filter_name_old != filter_name_new:
            dct_thread = self.dct_thread.get(execution_name, {})
            if dct_thread:
                filterchain = dct_thread.get("filterchain", None)
                if filterchain:
                    filterchain.remove_image_observer(observer, filter_name_old)
                    ret_value = filterchain.add_image_observer(observer, filter_name_new)
        return ret_value
    
    def remove_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to remove observer
            Param : 
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name , filter to remove
        """
        ret_value = False
        dct_thread = self.dct_thread.get(execution_name, {})
        if dct_thread:
            filterchain = dct_thread.get("filterchain", None)
            if filterchain:
                ret_value = filterchain.remove_image_observer(observer, filter_name)
        return ret_value
    
    def add_output_observer(self, execution_name):
        """
            attach the output information of execution to tcp_server
            supported only one observer. Add observer to tcp_server
        """
        ret_value = False
        dct_thread = self.dct_thread.get(execution_name, {})
        if dct_thread:
            filterchain = dct_thread.get("filterchain", None)
            if filterchain:
                if filterchain.get_filter_output_observers():
                    return True
                ret_value = filterchain.add_filter_output_observer(self.server_observer.send)
        return ret_value
        
    def remove_output_observer(self, execution_name):
        """
            remove the output information of execution to tcp_server
            supported only one observer. remove observer to tcp_server
        """
        
        ret_value = False
        dct_thread = self.dct_thread.get(execution_name, {})
        if dct_thread:
            filterchain = dct_thread.get("filterchain", None)
            if filterchain:
                if not filterchain.get_filter_output_observers():
                    return True
                ret_value = filterchain.remove_filter_output_observer(self.server_observer.send)
        return ret_value        
    
    ##########################################################################
    ########################## CONFIGURATION  ################################
    ##########################################################################
    def get_filterchain_list(self):
        return self.configuration.get_filterchain_list()
    
    def upload_filterchain(self, filterchain_name, s_file_contain):
        return self.configuration.upload_filterchain(filterchain_name, s_file_contain)
    
    def delete_filterchain(self, filterchain_name):
        return self.configuration.delete_filterchain(filterchain_name)
    
    def get_filter_list_from_filterchain(self, filterchain_name):
        return self.configuration.get_filters_from_filterchain(filterchain_name)
    
    def modify_filterchain(self, old_filterchain_name, new_filterchain_name, lst_str_filters):
        return self.configuration.modify_filterchain(old_filterchain_name, new_filterchain_name, lst_str_filters)
    
    ##########################################################################
    ############################ FILTERCHAIN  ################################
    ##########################################################################
    def load_chain(self, file_name):
        """
            return if chain is correctly loading.
        """
        new_chain = filterchain.read(file_name)
        if new_chain is not None and self.chain is not None:
            self.hook_new_chain(new_chain)
        self.chain = new_chain
        return self.chain_exists()

    def reload_filter(self, filtre=None):
        #NEED TO BE UPDATED
        # if filter is none, we reload all filters
        if self.chain is not None:
            self.chain.reload_filter(filtre)

    ##########################################################################
    ############################### FILTER  ##################################
    ##########################################################################
    def get_filter_list(self):
        return utils.load_filters().keys()

    
     