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

'''
Created on 2012-08-01

@author: benoit
'''

import inspect

def map_filter_to_ui(filter):
    import gui_filters
    for win in vars(gui_filters).values():
        if inspect.isclass(win):
            if win.__name__ == 'Win' + filter.__class__.__name__:
                return win
    return None

def load_filters():
    import filters
    return {name : filter for name, filter in vars(filters).items() if inspect.isclass(filter) or inspect.isfunction(filter)}

