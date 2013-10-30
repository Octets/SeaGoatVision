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

from SeaGoatVision.commons import log
from SeaGoatVision.commons.param import Param
import jsonrpclib
import threading
import numpy as np
import socket
import exceptions
logger = log.get_logger(__name__)

class Json_client():
    def __init__(self, port, host=""):
        self.rpc = jsonrpclib.Server('http://%s:%s' % (host, port))
        self._lst_port = []
        self.observer = []
        self._hostname = host

    def __getattr__(self, name):
        def cb_rpc():
            return getattr(self.rpc, name)
        return cb_rpc()

    def close(self):
        # Do nothing, cannot close the server.
        pass

    def add_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name to select the filter
        """
        port = self._get_port_streaming()
        local_observer = Observer(observer, self._hostname, port)

        status = self.rpc.add_image_observer(port, execution_name, filter_name)

        if not status:
            local_observer.stop()
        else:
            self.observer.append(local_observer)
            local_observer.start()
        return status

    def set_image_observer(self, observer, execution_name, filter_name_old, filter_name_new):
        find = False
        for o_observer in self.observer:
            if observer == o_observer.observer:
                find = True
                break
        if not find:
            logger.error("This observer doesn't exist.")
            return False
        return self.rpc.set_image_observer(execution_name, filter_name_old, filter_name_new)

    def remove_image_observer(self, observer, execution_name, filter_name):
        pass

    def get_params_filterchain(self, execution_name, filter_name):
        lst_param_ser = self.rpc.get_params_filterchain(execution_name, filter_name)
        return self._deserialize_param(lst_param_ser)

    def get_params_media(self, media_name):
        lst_param_ser = self.rpc.get_params_media(media_name)
        return self._deserialize_param(lst_param_ser)

    def _deserialize_param(self, lst_param_ser):
        return [Param("temp", None, serialize=param_ser) for param_ser in lst_param_ser]

    def _get_port_streaming(self):
        port = 5051 + len(self._lst_port)
        self._lst_port.append(port)
        return port

class Observer(threading.Thread):
    def __init__(self, observer, hostname, port):
        threading.Thread.__init__(self)
        self.observer = observer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.add = (hostname, port)
        self.close = False
        self.buffer = 65507

    def run(self):
        if self.observer:
            self.socket.sendto("I can see you.", self.add)
            while not self.close:
                sData = ""
                try:
                    data = self.socket.recv(self.buffer)
                    if not data:
                        continue

                    if data[0] != "b":
                        # print("wrong type index.")
                        continue

                    i = 1
                    while i < self.buffer and data[i] != "_":
                        i += 1

                    nb_packet_string = data[1:i]
                    if nb_packet_string.isdigit():
                        nb_packet = int(nb_packet_string)
                    else:
                        # print("wrong index.")
                        continue

                    sData += data[i + 1:]
                    for packet in range(1, nb_packet):
                        data, _ = self.socket.recvfrom(self.buffer)  # 262144 # 8192
                        if data[0] != "c":
                            # print("wrong type index continue")
                            continue

                        i = 1
                        while i < self.buffer and data[i] != "_":
                            i += 1

                        no_packet_string = data[1:i]
                        if no_packet_string.isdigit():
                            no_packet = int(no_packet_string)
                            # if no_packet != packet:
                                # print("Wrong no packet : %d" % packet)
                        else:
                            # print("wrong index continue.")
                            continue

                        sData += data[i + 1:]

                    self.observer(np.loads(sData))
                except Exception as e:
                    if type(e) is not exceptions.EOFError:
                        if not self.close:
                            logger.error("udp observer : %s", e)
        else:
            logger.error("self.observer is None.")

    def stop(self):
        self.close = True
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.socket.close()
            self.socket = None
        logger.info("Close client")
