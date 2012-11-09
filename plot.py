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

import numpy as np
import sys
import tempfile
import matplotlib.pyplot as plt

def create_graphic(data_file):
    data = np.fromfile(data_file)
    logging.error(len(data))
    data = data.reshape((2, len(data) / 2))
    precisions = data[:, 0]
    noises = data[:, 1]
    plt.clf()
    plt.plot(precisions, noises, '+b')
    plt.xlabel('Precision (%)')
    plt.ylabel('Noise (%)')
    ntf = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(ntf.file)
    ntf.flush()
    file_name = ntf.name
    ntf.close()
    return file_name

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='/home/benoit/error.txt')
    data_file = sys.argv[1] 
    f = open('/home/benoit/test22.txt', 'w')
    f.write('ohai!')
    f.flush()
    try:
        image_file = create_graphic(data_file)
    except Exception, e:
        logging.exception(data_file)
    f.write(data_file)
    f.write(image_file)
    f.flush()
    f.close()

    print image_file
    sys.stdout.flush()
    
    