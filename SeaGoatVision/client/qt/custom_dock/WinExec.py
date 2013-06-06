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

from SeaGoatVision.client.qt.utils import get_ui

class WinExec:

    def __init__(self):

        #self.filtre = filtre
        #self.filtre_init = copy.copy(filtre)
        #self.cb = cb

        self.ui = get_ui(self)
        #self.window = ui.get_object(win_name(self))
        #self.txtCurrent = ui.get_object('txtCurrent')
        #self.txtWorking = ui.get_object('txtWorking')

        #self.init_window()

    def init_window(self):
        self.txtCurrent.get_buffer().set_text(self.filtre.code)
        self.txtWorking.get_buffer().set_text(self.filtre.code)

    def on_btnOK_clicked(self, widget):
        self.cb()
        self.window.destroy()

    def on_btnCancel_clicked(self, widget):
        self.filtre.code = self.filtre_init.code
        self.init_window()

    def on_btnApply_clicked(self, widget):
        start, end = self.txtWorking.get_buffer().get_bounds()
        code = self.txtWorking.get_buffer().get_text(start, end, False)
        self.txtCurrent.get_buffer().set_text(code)
        self.filtre.set_code(code)
