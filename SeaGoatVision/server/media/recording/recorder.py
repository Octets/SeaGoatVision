#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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

# not supported


class Recorder:

    def __init__(self):
        self.savepath = ''
        self.saver_class = None
        self.savers = {}
        self.running = False

    def set_saver_class(self, saver):
        self.saver_class = saver

    def set_save_path(self, savepath):
        self.savepath = savepath

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def add_filter(self, filtre):
        self.savers[filtre] = self.saver_class(self.savepath, filtre)

    def remove_filter(self, filtre):
        del self.savers[filtre]

    def filter_observer(self, filtre, image):
        if not self.running:
            return

        if self.saver is not None and filtre in self.filters.keys:
            self.saver.save(filtre, image)
