import os
os.chdir(os.path.join(os.getcwd(), ".."))
os.sys.path.insert(0,os.getcwd()) 

import filters
import unittest

class TestFilters(unittest.TestCase):
    
    def test_load_filters(self):
        fs = filters.load_filters()
        for n, f in fs.items():
            print 'name: ' + n + ' filter: ' + f.__name__
    