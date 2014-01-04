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

from PySide import QtUiTools
from PySide import QtCore

import os
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)


def tree_selected_index(treeview):
    (model, iter) = treeview.get_selection().get_selected()
    if iter is None:
        return -1
    path = model.get_path(iter)
    return path.get_indices()[0]


def tree_row_selected(treeview):
    (model, iter) = treeview.get_selection().get_selected()
    return iter is not None


def get_ui(widget):
    loader = QtUiTools.QUiLoader()
    uiPath = os.path.join(
        'SeaGoatVision',
        'client',
        'qt',
        'uifiles',
        win_name(widget) + '.ui')
    logger.info("Loading ui %s", uiPath)
    uiFile = QtCore.QFile(uiPath)
    uiFile.open(QtCore.QFile.ReadOnly)
    return loader.load(uiFile)


def win_name(window):
    return window.__class__.__name__
