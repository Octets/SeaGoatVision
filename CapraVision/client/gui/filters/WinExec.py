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

from gi.repository import GtkSource

import copy
from CapraVision.client.gui.utils import *

class WinExec:
    
    def __init__(self, filtre, cb):
        self.filtre = filtre
        self.filtre_init = copy.copy(filtre)
        self.cb = cb
        
        ui = get_ui(self)
        self.window = ui.get_object(win_name(self))
        self.scwCurrent = ui.get_object('scwCurrent')
        self.scwWorking = ui.get_object('scwWorking')
        
        self.txtCurrent = GtkSource.View.new_with_buffer(GtkSource.Buffer())
        self.txtCurrent.set_editable(False)
        self.txtCurrent.set_can_focus(False)
        self.txtCurrent.set_show_line_numbers(True)
        
        self.txtWorking = GtkSource.View.new_with_buffer(GtkSource.Buffer())
        self.txtWorking.set_insert_spaces_instead_of_tabs(True)
        self.txtWorking.set_indent_on_tab(True)
        self.txtWorking.set_indent_width(4)
        self.txtWorking.set_show_line_numbers(True)
        self.txtWorking.set_can_default(True)
        
        lang_manager = GtkSource.LanguageManager()
        self.txtCurrent.get_buffer().set_language(
                                        lang_manager.get_language('python'))
        self.txtWorking.get_buffer().set_language(
                                        lang_manager.get_language('python'))
        self.scwCurrent.add(self.txtCurrent)
        self.scwWorking.add(self.txtWorking)
        
        self.window.set_default(self.txtWorking)
        self.window.set_focus(self.txtWorking)
        
        self.init_window()
        
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
    