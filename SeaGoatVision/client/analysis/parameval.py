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

import cv2
import numpy as np
import os
import subprocess
import tempfile

import linetest


class ParameterEvaluation:

    def __init__(self, test_folder, chain, fname, pname, minval, maxval):
        """
        Args:
            test_folder: test folder path
            chain: the filterchain object to test
            fname: the filter name
            pname: the parameter name to evaluate
            minval: the starting value
            maxval: the ending value"""
        self.test_folder = test_folder
        self.chain = chain
        self.fname = fname
        self.pname = pname
        self.filter = self.filter_to_use()
        self.minval = minval
        self.maxval = maxval
        self.precisions = np.zeros(maxval - minval, dtype=np.float16)
        self.noises = np.zeros(maxval - minval, dtype=np.float16)

    def launch(self):
        test = linetest.LineTest(self.test_folder, self.chain)
        orig_val = getattr(self.filter, self.pname).get_current_value()
        for i in xrange(int(self.minval), int(self.maxval)):
            idx = i - self.minval
            getattr(self.filter, self.pname).set_current_value(i)
            if hasattr(self.filter, 'configure'):
                self.filter.configure()
            test.launch()
            self.precisions[idx] = round(test.avg_precision() * 100.0, 2)
            self.noises[idx] = round(test.avg_noise() * 100.0, 2)

        getattr(self.filter, self.pname).set_current_value(orig_val)
        if hasattr(self.filter, 'configure'):
            self.filter.configure()

    def filter_to_use(self):
        for f in self.chain.filters:
            if f.__class__.__name__ == self.fname:
                return f
        return

    def save_data(self):
        tmp = tempfile.NamedTemporaryFile()
        data = np.append(self.precisions, self.noises)
        tmp.file.write(data.tostring())
        tmp.file.flush()
        return tmp

    def create_graphic(self):
        data_file = self.save_data()
        proc = subprocess.Popen(('python', 'plot.py', data_file.name),
                                stdout=subprocess.PIPE)
        image_file = proc.stdout.readline()[:-1]
        print image_file
        data_file.close()
        img = cv2.imread(image_file)
        os.remove(image_file)
        # return img
        return cv2.resize(img, (600, 450))
