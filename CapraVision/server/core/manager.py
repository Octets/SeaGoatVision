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
    def get_source_list(self):
        return imageproviders.load_sources().keys()

    ##########################################################################
    ############################### THREAD  ##################################
    ##########################################################################
    
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
    
     
