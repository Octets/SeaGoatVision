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
Date : Novembre 2012
"""

from CapraVision.server.core.mainloop import MainLoop
from CapraVision.server import imageproviders
import filterchain
from CapraVision.server.filters import utils

class VisionManager:

    def __init__(self):
        self.chain = None
        self.create_new_chain()
        self.source = None
        self.thread = MainLoop()
        self.thread.add_observer(self.thread_observer)

    def get_source(self):
        return self.source

    def get_chain(self):
        return self.chain

    def get_thread(self):
        return self.thread

    def change_sleep_time(self, sleep_time):
        self.thread.change_sleep_time(sleep_time)

    def start_thread(self):
        self.thread.start(self.source)

    def stop_thread(self):
        self.thread.stop()

    def __getitem__(self, index):
        return self.chain.__getitem__(index)

    def get_filter_from_index(self, index):
        return self.chain.__getitem__(index)

    def get_filter_list(self):
        return utils.load_filters().keys()

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
        new_chain = filterchain.read(file_name)
        if new_chain is not None and self.chain is not None:
            self.hook_new_chain(new_chain)
        self.chain = new_chain

    def save_chain(self, file_name):
        filterchain.write(file_name, self.chain)

    def change_source(self, new_source):
        if self.source <> None:
            imageproviders.close_source(self.source)
        if new_source <> None:
            self.source = imageproviders.create_source(new_source)
            self.thread.start(self.source)
        else:
            self.source = None

    def is_thread_running(self):
        return self.thread.is_running()

    def thread_observer(self, image):
        if self.chain is not None and image is not None:
            self.chain.execute(image)

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

    def add_thread_observer(self, observer):
        self.thread.add_observer(observer)

    def remove_thread_observer(self, observer):
        self.thread.remove_observer(observer)

    def close_server(self):
        self.stop_thread()

    def is_connected(self):
        return True

