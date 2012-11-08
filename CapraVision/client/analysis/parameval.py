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

import cv2
#import matplotlib.pyplot as plt
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
        self.precisions = {}
        self.noises = {}
        
    def launch(self):
        test = linetest.LineTest(self.test_folder, self.chain)
        for i in xrange(self.minval, self.maxval):
            setattr(self.filter, self.pname, i)
            if hasattr(self.filter, 'configure'):
                self.filter.configure()
            test.launch()
            self.precisions[i] = test.avg_precision()
            self.noises[i] = test.avg_noise()
            
    def filter_to_use(self):
            for f in self.chain.filters:
                if f.__name__ == self.fname:
                    return f
            return None
        
    def create_graphic(self):
        #plt.clf()
        #plt.plot(self.precisions, self.noises, '+b')
        #plt.xlabel('Precision (%)')
        #plt.ylabel('Noise (%)')
        
        ntf = tempfile.NamedTemporaryFile(suffix='.png')
        #plt.savefig(ntf.file)
        ntf.flush()
        image = cv2.imread(ntf.name)
        ntf.close()
        return image
    