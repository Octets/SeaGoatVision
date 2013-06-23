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

import time

import socket
from threading import Thread
import logging

logger = logging.getLogger("seagoat")

BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

class Server:

    def __init__(self):
        self.handlers = []

    def start(self, ip, port):
        t = Thread(target=self.innerStart, args=(ip, port, ))
        t.start()

    def innerStart(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reuse the socket if already open - fix when closed without close.
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ip, port))
        logger.info("Server awaiting connections on port %s", str(port))

        self.done = False

        while not self.done:
            self.socket.listen(1)
            self.socket.settimeout(2)
            try:
                conn, addr = self.socket.accept()
                logger.info('Connected to: %s', addr)
                handler = ClientHandler(conn)
                self.handlers.append(handler)
                t = Thread(target=handler.handle)
                t.start()
            except:
                pass #Do nothing if no user is added

    def stop(self):
        self.done = True
        self.socket.close()
        for handler in self.handlers:
            handler.stop()

    def send(self, data):
        for handler in self.handlers:
            try:
                handler.send("%s\n" % data)
            except:
                handler.stop()
                if handler in self.handlers:
                    self.handlers.remove(handler)
                logger.info("Client disconnected %s", handler)

class ClientHandler:

    def __init__(self, conn):
        self.done = False
        self.conn = conn

    def handle(self):
        while not self.done:
            try:
                _ = self.conn.recv(BUFFER_SIZE)
            except:
                time.sleep(1)
                pass #Do noting if no data is received

            #if not data: break
            #print "received data:", data
            #self.conn.send(data)  # echo
            #self.conn.close()

    def stop(self):
        self.done = True
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.conn.close()

    def send(self, data):
        self.conn.send(data)
