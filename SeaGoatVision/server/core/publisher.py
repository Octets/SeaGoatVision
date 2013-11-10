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
from SeaGoatVision.commons import keys
from SeaGoatVision.commons import log

CST_TOPIC_KEY = "topic"
CST_NB_CLIENT_KEY = "client"

logger = log.get_logger(__name__)

# TODO missing unsubscribe and deregister
class Publisher():
    def __init__(self, port):
        # list of key associated with topic number
        self.dct_key_topic = {}
        self.context = zmq.Context()
        self.dct_global_key = keys.get_lst_key_topic_pubsub()
        self.port = port
        self.socket = None
        # start topic at 100, reserve the first for global
        self.new_topic_no = 100

    def register(self, key):
        topic = self._get_topic(key)
        if topic:
            logger.warning("Key already exist : %s" % key)
            return topic
        topic = self.dct_global_key.get(key, None)
        if not topic:
            topic = self.new_topic_no
            self.new_topic_no += 1
        self.dct_key_topic[key] = {CST_TOPIC_KEY:topic, CST_NB_CLIENT_KEY:0}

    def subscribe(self, key):
        topic = self._get_topic(key)
        if not topic:
            logger.warning("Cannot subscribe, key not exist : %s" % key)
            return 0
        self._incr_topic(key)
        return topic

    def publish(self, key, data):
        if not self.socket:
            return False
        #logger.debug("Send to key %s data %s." % (key, data))
        topic = self._get_topic_if_client_in_topic(key)
        if not topic:
            logger.warning("Key not exist : %s" % key)
            return False
        self.socket.send("%s %s" % (topic, data))
        return True

    def start(self):
        if self.socket:
            return False
        logger.info("Publisher on port %d is ready." % self.port)
        # Ignore the zmq.PUB error in Eclipse.
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % self.port)
        return True

    def stop(self):
        if not self.socket:
            return False
            self.socket.close()
            self.socket = None
        return True

    def get_callback_publish(self, key):
        # get a callback with the same key
        # caution, always use self.publish to use validation
        publish = self.publish
        def cb_publish(data):
            publish(key, data)
        return cb_publish

    def _get_topic(self, key):
        dct_data = self.dct_key_topic.get(key, None)
        if not dct_data:
            return None
        return dct_data.get(CST_TOPIC_KEY, None)

    def _incr_topic(self, key):
        dct_data = self.dct_key_topic.get(key, None)
        if not dct_data:
            return None
        dct_data[CST_NB_CLIENT_KEY] += 1

    def _get_topic_if_client_in_topic(self, key):
        dct_data = self.dct_key_topic.get(key, None)
        if not dct_data:
            return None
        if dct_data[CST_NB_CLIENT_KEY]:
            return dct_data.get(CST_TOPIC_KEY, None)
        return None
