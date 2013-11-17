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
Description : ZeroMQ publisher implementation
"""

import zmq
import threading
from SeaGoatVision.commons import log

CST_TOPIC_KEY = "topic"
CST_NB_CLIENT_KEY = "client"

logger = log.get_logger(__name__)

class Subscriber():
    def __init__(self, controller, port, addr="localhost"):
        self.controller = controller
        # list of key associated with topic number
        # example : {"key":(topic, [callback1, callback2])}
        self.dct_key_topic_cb = {}
        self.port = port
        self.server = Listen_output(self._recv_callback_topic, addr, port)

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

    def subscribe(self, key, callback):
        if self._add_callback(key, callback):
            # callback already added
            return True
        topic = self.controller.subscribe(key)
        if not topic:
            logger.error("Cannot access to the publisher %s" % key)
            return False
        self.dct_key_topic_cb[key] = (topic, [callback])
        self.server.add_subscriber(topic)
        return True
        
    def _add_callback(self, key, callback):
        lst_topic = self.dct_key_topic_cb.get(key, None)
        if lst_topic is None:
            return False
        lst_cb = lst_topic[1]
        if callback not in lst_cb:
            lst_cb.append(callback)
        else:
            logger.warning("Callback already added on key %s : %s" % (key, callback))
        return True

    def _recv_callback_topic(self, data):
        # substract the topic
        pos_first_space = data.find(" ")
        # find all callback of this topic
        topic = int(data[:pos_first_space])
        message = data[pos_first_space + 1:]
        for lst_topic in self.dct_key_topic_cb.values():
            if lst_topic[0] == topic:
                for cb in lst_topic[1]:
                    cb(message) 

class Listen_output(threading.Thread):
    def __init__(self, observer, addr, port):
        threading.Thread.__init__(self)
        # Ignore the zmq.PUB error in Eclipse.
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.is_stopped = False
        self.observer = observer
        self.addr = addr
        self.port = port

    def run(self):
        self.socket.connect("tcp://%s:%s" % (self.addr, self.port))
        while not self.is_stopped:
            try:
                data = self.socket.recv()
                if data:
                    self.observer(data)
            except zmq.error.ZMQError:
                #ignore it, it's the timeout
                pass
            except Exception as e:
                log.printerror_stacktrace(logger, e)
                self.is_stopped = True
        self.socket.close()

    def add_subscriber(self, no):
        self.socket.setsockopt(zmq.SUBSCRIBE, str(no))

    def remove_subscriber(self, no):
        self.socket.setsockopt(zmq.UNSUBSCRIBE, str(no))

    def stop(self):
        self.is_stopped = True
