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
Description : Server Service implementation using vServer_pb2, generate by .proto file
Authors: Mathieu Benoit (mathben963@gmail.com)
Date : October 2012
"""

# Import required RPC modules
from CapraVision.proto import server_pb2
from CapraVision.server.core.manager import VisionManager

class ProtobufServerImpl(server_pb2.CommandService):
    def __init__(self, * args, ** kwargs):
        server_pb2.CommandService.__init__(self, * args, ** kwargs)

        self.manager = VisionManager()

    def get_source(self, controller, request, done):
        pass

    def get_chain(self, controller, request, done):
        pass

    def get_thread(self, controller, request, done):
        pass

    def change_sleep_time(self, controller, request, done):
        pass

    def start_thread(self, controller, request, done):
        pass

    def stop_thread(self, controller, request, done):
        oass

    def get_filter_from_index(self, controller, request, done):
        pass

    def get_filter_list(self, controller, request, done):
        print("get_filter_list request %s" % request)

        # Create a reply
        response = server_pb2.GetFilterListResponse()
        for filter in self.manager.get_filter_list():
            response.filters.append(filter)

        # We're done, call the run method of the done callback
        done.run(response)

    def get_filter_list_from_filterchain(self, controller, request, done):
        print("get_filter_list_from_filterchain request %s" % request)

        # Create a reply
        response = server_pb2.GetFilterListFromFilterChainResponse()
        for item in self.manager.get_filter_list_from_filterchain():
            response.filters.add(name=item.name, doc=item.doc)

        # We're done, call the run method of the done callback
        done.run(response)

    def count_filters(self, controller, request, done):
        pass

    def create_new_chain(self, controller, request, done):
        self.manager.create_new_chain()

    def hook_new_chain(self, controller, request, done):
        pass

    def chain_exists(self, controller, request, done):
        pass

    def load_chain(self, controller, request, done):
        print("load_chain request %s" % request)

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            response.status = int(not self.manager.load_chain(request.filterName))
        except Exception, e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def save_chain(self, controller, request, done):
        pass

    def change_source(self, controller, request, done):
        pass

    def is_thread_running(self, controller, request, done):
        pass

    def thread_observer(self, controller, request, done):
        pass

    def add_filter(self, controller, request, done):
        pass

    def remove_filter(self, controller, request, done):
        pass

    def reload_filter(self, controller, request, done):
        print("reload_filter request %s" % request)

        # Create a reply
        response = server_pb2.StatusResponse()
        try:
            self.manager.reload_filter(request.filterName)
            response.status = 0
        except Exception, e:
            print "Exception: ", e
            response.status = -1

        # We're done, call the run method of the done callback
        done.run(response)

    def move_filter_up(self, controller, request, done):
        pass

    def move_filter_down(self, controller, request, done):
        pass

    def add_image_observer(self, controller, request, done):
        pass

    def remove_image_observer(self, controller, request, done):
        pass

    def add_filter_observer(self, controller, request, done):
        pass

    def remove_filter_observer(self, controller, request, done):
        pass

    def add_filter_output_observer(self, controller, request, done):
        pass

    def remove_filter_output_observer(self, controller, request, done):
        pass

    def add_thread_observer(self, controller, request, done):
        pass

    def remove_thread_observer(self, controller, request, done):
        pass

    def close_server(self, controller, request, done):
        self.manager.close_server()

    def is_connected(self, controller, request, done):
        print("is_connected request %s" % request)

        # Create a reply
        response = server_pb2.StatusResponse()
        response.status = 0
        # We're done, call the run method of the done callback
        done.run(response)

