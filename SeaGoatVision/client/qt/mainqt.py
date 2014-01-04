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
Description : launch qt client
"""
import sys

from PySide.QtGui import QApplication
import main
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


def run(ctr, subscriber, local=False, host="localhost", port=8090):
    app = QApplication(sys.argv)
    win = main.WinMain(ctr, subscriber, host=host, islocal=local)
    win.show()
    try:
        rint = app.exec_()
    except Exception as e:
        logger.critical("Exit error : %s" % e)
    # close the server
    win.quit()
    ctr.close()

    return rint
