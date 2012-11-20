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

import threading
import time

class MainLoop:
    
    def __init__(self):
        self.sleep_time = 1 / 30.0
        self.observers = []
        self.thread = None
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
            
    def notify_observers(self, image):
        for observer in self.observers:
            observer(image)

    def start(self, source):
        self.stop()
        self.thread = ThreadMainLoop(source, self.sleep_time, self.notify_observers)
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread = None
            
    def change_sleep_time(self, sleep_time):
        self.sleep_time = sleep_time
        if self.thread is not None:
            self.thread.sleep_time = sleep_time        
    
    def is_running(self):
        return self.thread is not None and self.thread.running
    
class ThreadMainLoop(threading.Thread):
    """Main thread to process the images.
    
    Args:
        source: the source to receive images from.
        filterchain: the configured filterchain
        sleep_time: time to wait in seconds before getting the next image
    """
    def __init__(self, source, sleep_time, observer):
        threading.Thread.__init__(self)
        self.daemon = True
        self.source = source
        self.running = False
        self.observer = observer
        self.sleep_time = sleep_time
        
    def run(self):
        self.running = True
        for image in self.source:
            if image is None:
                time.sleep(self.sleep_time)
                continue
            self.observer(image)
            if not self.running:
                break
            if self.sleep_time >= 0:
                time.sleep(self.sleep_time)
        self.running = False
        self.observer(None)
        
    def stop(self):
        self.running = False
