#!/usr/bin/env python

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
Description : This controller use protobuf to communicate to the vision server
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

# Import required RPC modules
from protobuf.socketrpc import RpcService
from CapraVision.proto import server_pb2

# Configure logging
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Import CapraVision library - temporaire, remove me
from CapraVision.server.core.manager import VisionManager

# The callback is for asynchronous call to RpcService
def callback(request, response):
    """Define a simple async callback."""
    log.info('Asynchronous response :' + response.__str__())

class Controller():
    def __init__(self):
        # Server details
        hostname = 'localhost'
        port = 8090

        # Create a new service instance
        self.service = RpcService(server_pb2.CommandService_Stub, port, hostname)

        self.manager = VisionManager()

    def get_source(self):
        return self.manager.get_source()

    def get_chain(self):
        return self.manager.get_chain()

    def get_thread(self):
        return self.manager.get_thread()

    def change_sleep_time(self, sleep_time):
        self.manager.change_sleep_time(sleep_time)

    def start_thread(self):
        self.manager.start_thread()

    def stop_thread(self):
        self.manager.stop_thread()

    def __getitem__(self, index):
        return self.manager.get_filter_from_index(index)

    def get_filter_from_index(self, index):
        return self.manager.get_filter_from_index(index)

    def get_filter_list(self):
        """
            Return list of filter
        """
        request = server_pb2.GetFilterListRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filter_list(request, timeout=10000)
            returnValue = response.filters

        except Exception, ex:
            log.exception(ex)

        return returnValue

    def count_filters(self):
        return self.manager.count_filters()

    def create_new_chain(self):
        self.manager.create_new_chain()

    def hook_new_chain(self, new_chain):
        self.manager.hook_new_chain(new_chain)

    def chain_exists(self):
        self.manager.chain_exists()

    def load_chain(self, file_name):
        self.manager.load_chain(file_name)

    def save_chain(self, file_name):
        self.manager.save_chain(file_name)

    def change_source(self, new_source):
        self.manager.change_source(new_source)

    def is_thread_running(self):
        return self.manager.is_thread_running()

    def thread_observer(self, image):
        self.manager.thread_observer(image)

    def add_filter(self, filtre):
        self.manager.add_filter(filtre)

    def remove_filter(self, filtre):
        self.manager.remove_filter(filtre)

    def reload_filter(self, filtre=None):
        self.manager.reload_filter(filtre)

    def move_filter_up(self, filtre):
        self.manager.move_filter_up(filtre)

    def move_filter_down(self, filtre):
        self.manager.move_filter_down(filtre)

    def add_image_observer(self, observer):
        self.manager.add_image_observer(observer)

    def remove_image_observer(self, observer):
        self.manager.remove_image_observer(observer)

    def add_filter_observer(self, observer):
        self.manager.add_filter_observer(observer)

    def remove_filter_observer(self, observer):
        self.manager.remove_filter_observer(observer)

    def add_filter_output_observer(self, output):
        self.manager.add_filter_output_observer(output)

    def remove_filter_output_observer(self, output):
        self.manager.remove_filter_output_observer(output)

    def add_thread_observer(self, observer):
        self.manager.add_thread_observer(observer)

    def remove_thread_observer(self, observer):
        self.manager.remove_thread_observer(observer)

    def close_server(self):
        self.manager.close_server()

    def is_connected(self):
        print("Try connection")
        request = server_pb2.IsConnectedRequest()
        # Make an synchronous call
        response = None
        try:
            response = self.service.is_connected(request, timeout=10000) is not None
            if response:
                print("Connection sucessful")
        except Exception, ex:
            log.exception(ex)

        return response
    