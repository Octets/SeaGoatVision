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

class Manager:

    def __init__(self):
        self.dct_thread = {}
        self.configuration = Configuration()
        
        self.chain = None
        self.create_new_chain()
        self.source = None
        self.thread = MainLoop()
        self.thread.add_observer(self.thread_observer)
    
    ##########################################################################
    ################################ CLIENT ##################################
    ##########################################################################
    def is_connected(self):
        return True
    
    ##########################################################################
    ############################# SERVER STATE ###############################
    ##########################################################################
    def close(self):
        # close all thread
        for thread in self.dct_thread.values():
            thread["thread"].quit()
            thread["observer"].stop()
        print("All thread is closed.")
    
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
        observer = Observer_image_provider()
        self.dct_thread[execution_name] = {"thread" : thread, "observer" : observer}
        
        filterchain.add_image_observer(observer.observer)
        thread.add_observer(filterchain.execute)
        thread.start(source)
        
        return observer
    
    def stop_filterchain_execution(self, execution_name):
        thread = self.dct_thread.get(execution_name, None)
        
        if not thread:
            # change this, return the actual thread
            print("The execution %s is already stopped." % execution_name)
            return None
        
        thread["thread"].quit()
        thread["observer"].stop()
        del self.dct_thread[execution_name]
        
        
    ##########################################################################
    ################################ SOURCE ##################################
    ##########################################################################
    def get_source(self):
        return self.source

    def change_source(self, new_source):
        if self.source <> None:
            imageproviders.close_source(self.source)
        if new_source <> None:
            self.source = imageproviders.create_source(new_source)
            self.thread.start(self.source)
        else:
            self.source = None
            
    def get_source_list(self):
        return imageproviders.load_sources().keys()

    ##########################################################################
    ############################### THREAD  ##################################
    ##########################################################################
    def get_thread(self):
        return self.thread

    def change_sleep_time(self, sleep_time):
        self.thread.change_sleep_time(sleep_time)

    def start_thread(self):
        self.thread.start(self.source)

    def stop_thread(self):
        self.thread.stop()

    def is_thread_running(self):
        return self.thread.is_running()

    def thread_observer(self, image):
        if self.chain is not None and image is not None:
            self.chain.execute(image)

    def add_thread_observer(self, observer):
        self.thread.add_observer(observer)

    def remove_thread_observer(self, observer):
        self.thread.remove_observer(observer)

    def close_server(self):
        self.stop_thread()
    
    ##########################################################################
    ########################## CONFIGURATION  ################################
    ##########################################################################
    def list_filterchain(self):
        return self.configuration.list_filterchain()
    
    def upload_filterchain(self, filterchain_name, s_file_contain):
        return self.configuration.upload_filterchain(filterchain_name, s_file_contain)
    
    def delete_filterchain(self, filterchain_name):
        return self.configuration.delete_filterchain(filterchain_name)
    
    def get_filters_from_filterchain(self, filterchain_name):
        return self.configuration.get_filters_from_filterchain(filterchain_name)
    
    def edit_filterchain(self, old_filterchain_name, new_filterchain_name, lst_str_filters):
        return self.configuration.edit_filterchain(old_filterchain_name, new_filterchain_name, lst_str_filters)
    
    ##########################################################################
    ############################ FILTERCHAIN  ################################
    ##########################################################################
    def get_chain(self):
        return self.chain

    def get_filter_from_index(self, index):
        return self.chain.__getitem__(index)

    def get_filter_list_from_filterchain(self):
        return self.chain.get_filter_list()

    def count_filters(self):
        if self.chain is not None:
            return self.chain.count()
        return -1

    def create_new_chain(self):
        new_chain = filterchain.FilterChain()
        if self.chain is not None:
            self.hook_new_chain(new_chain)
        self.chain = new_chain

    def hook_new_chain(self, new_chain):
        for o in self.chain.get_image_observers():
            new_chain.add_image_observer(o)
        for o in self.chain.get_filter_observers():
            new_chain.add_filter_observer(o)
        for o in self.chain.get_filter_output_observers():
            new_chain.add_filter_output_observer(o)

    def chain_exists(self):
        return self.chain is not None

    def load_chain(self, file_name):
        """
            return if chain is correctly loading.
        """
        new_chain = filterchain.read(file_name)
        if new_chain is not None and self.chain is not None:
            self.hook_new_chain(new_chain)
        self.chain = new_chain
        return self.chain_exists()

    def save_chain(self, file_name):
        filterchain.write(file_name, self.chain)
        
    def add_filter(self, filtre):
        if self.chain is not None:
            self.chain.add_filter(filtre)

    def remove_filter(self, filtre):
        if self.chain is not None:
            self.chain.remove_filter(filtre)

    def reload_filter(self, filtre=None):
        # if filter is none, we reload all filters
        if self.chain is not None:
            self.chain.reload_filter(filtre)

    def move_filter_up(self, filtre):
        if self.chain is not None:
            self.chain.move_filter_up(filtre)

    def move_filter_down(self, filtre):
        if self.chain is not None:
            self.chain.move_filter_down(filtre)

    def add_image_observer(self, observer):
        if self.chain is not None:
            self.chain.add_image_observer(observer)

    def remove_image_observer(self, observer):
        if self.chain is not None:
            self.chain.remove_image_observer(observer)

    def add_filter_observer(self, observer):
        if self.chain is not None:
            self.chain.add_filter_observer(observer)

    def remove_filter_observer(self, observer):
        if self.chain is not None:
            self.chain.remove_filter_observer(observer)

    def add_filter_output_observer(self, output):
        if self.chain is not None:
            self.chain.add_filter_output_observer(output)

    def remove_filter_output_observer(self, output):
        if self.chain is not None:
            self.chain.remove_filter_output_observer(output)
            
    ##########################################################################
    ############################### FILTER  ##################################
    ##########################################################################
    def get_filter_list(self):
        return utils.load_filters().keys()




class Observer_image_provider():
    def __init__(self):
        self.image = None
        self.lastImage = None
        self.isStopped = False
        self.sleep_time = 1 / 30.0
        self.sFilter = ""
    
    def observer(self, filter, image):
        if self.sFilter == filter:
            self.image = image
    
    def next(self):
        # check if the image is different of precedent
        epsilon = 1e-6
        diffArray = epsilon
        while not self.isStopped:
             if self.image is not None:
                 if self.lastImage is None:
                     # its the first picture
                     break
                 
                 diffArray = self.image - self.lastImage
                 max = numpy.max(numpy.abs(diffArray))
                 if max > epsilon:
                     # The picture is different
                     break
             time.sleep(self.sleep_time)
            
        self.lastImage = self.image

        return self.image
    
    def set_filter_name(self, sFilter):
        self.sFilter = sFilter
        print("New filter : %s" % sFilter)
    
    def stop(self):
        self.isStopped = True
    
     
