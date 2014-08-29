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


def get_ui(widget, force_name=None):
    if force_name is None:
        force_name = win_name(widget)
    loader = QtUiTools.QUiLoader()
    ui_path = os.path.join(
        'SeaGoatVision',
        'client',
        'qt',
        'uifiles',
        force_name + '.ui')
    logger.info("Loading ui %s", ui_path)
    ui_file = QtCore.QFile(ui_path)
    ui_file.open(QtCore.QFile.ReadOnly)
    return loader.load(ui_file)


def win_name(window):
    return window.__class__.__name__
