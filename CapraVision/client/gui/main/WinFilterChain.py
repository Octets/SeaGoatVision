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

from CapraVision.client.gui.utils import *

from CapraVision.core import filterchain

from CapraVision import filters

from WinFilterSel import WinFilterSel
from WinLineTest import WinLineTest
from WinMapper import WinMapper
from WinViewer import WinViewer
from CapraVision.server.tcp_server import Server

class WinFilterChain:
    """Main window
    Allow the user to create, edit and test filter chains
    """
    
    WINDOW_TITLE = "Capra Vision"

    def __init__(self):
        ui = get_ui(self, 'filterChainListStore', 
                    'imgOpen', 'imgNew', 'imgUp', 'imgDown')
        self.window = ui.get_object(win_name(self))
        self.lstFilters = ui.get_object('lstFilters')
        self.btnView = ui.get_object('btnView')
        self.btnAdd = ui.get_object('btnAdd')
        self.btnRemove = ui.get_object('btnRemove')
        self.btnConfig = ui.get_object('btnConfig')
        self.btnUp = ui.get_object('btnUp')
        self.btnDown = ui.get_object('btnDown')
        self.txtFilterChain = ui.get_object('txtFilterChain')
        self.menuTools = ui.get_object('menuTools')
        
        self.win_list = []
        
        self.filterChainListStore = ui.get_object('filterChainListStore')
        self.set_state_empty()
        self.change_state()
        
        self.server = Server()
        self.server.start("127.0.0.1", 5030)
        

    def add_window_to_list(self, win):
        self.win_list.append(win.window)
        
    def change_state(self):
        tools_enabled = self.state <> WindowState.Empty
        self.btnAdd.set_sensitive(tools_enabled)
        self.btnConfig.set_sensitive(tools_enabled)
        self.btnDown.set_sensitive(tools_enabled)
        self.btnRemove.set_sensitive(tools_enabled)
        self.btnUp.set_sensitive(tools_enabled)
        self.btnView.set_sensitive(tools_enabled)

    def del_current_row(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        self.fchain.remove_filter(self.selected_filter())
        
    def filter_modif_callback(self):
        self.set_state_modified()
        
    def filters_changed_observer(self):
        self.show_filter_chain()

    def is_state_modified_or_created(self):
        return (self.state == WindowState.Create or
            self.state == WindowState.Modified)

    def msg_confirm_create_new(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                                   Gtk.ButtonsType.YES_NO, 
                                   "Create new filterchain?")
        result = dialog.run()
        dialog.destroy()
        return result
        
    def msg_confirm_save_before_closing(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                                   None, 
                                   "Save changes?")
        dialog.add_button('Close without saving', Gtk.ResponseType.CLOSE)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        dialog.format_secondary_text(
            "Do you want to save the current filterchain before closing?")
        result = dialog.run()
        dialog.destroy()
        return result
    
    def msg_confirm_save_before_new(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                                   None, 
                                   "Save changes?")
        dialog.add_button(Gtk.STOCK_NO, Gtk.ResponseType.NO)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_YES, Gtk.ResponseType.YES)
        dialog.format_secondary_text(
            "Do you want to save the current filterchain before proceeding?")
        result = dialog.run()
        dialog.destroy()
        return result

    def msg_warn_del_row(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING, 
                            Gtk.ButtonsType.YES_NO, "Delete selected filter")
        dialog.format_secondary_text(
                                "Do you want to remove the selected filter?")
        result = dialog.run()
        dialog.destroy()
        return result

    def save_chain(self):
        if self.state == WindowState.Empty:
            return True
        elif self.state == WindowState.Create:
            return self.save_chain_as()
        else:
            filterchain.write(self.txtFilterChain.get_text(), self.fchain)
            self.set_state_show()
            return True

    def save_chain_as(self):
        if self.state == WindowState.Empty:
            return True
        dialog = Gtk.FileChooserDialog("Save filterchain", None,
                                   Gtk.FileChooserAction.SAVE,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = dialog.run()
        fname = dialog.get_filename()
        dialog.destroy()
        
        if response == Gtk.ResponseType.OK:
            if not fname.endswith('.filterchain'):
                fname += '.filterchain'
            filterchain.write(fname, self.fchain)
            self.txtFilterChain.set_text(fname)
            self.set_state_show()
            return True
        else:
            return False

    def selected_filter(self):
        (model, iter) = self.lstFilters.get_selection().get_selected()
        if iter is None:
            return None
        path = model.get_path(iter)
        return self.fchain.filters[path.get_indices()[0]]
    
    def set_state_create(self):
        self.state = WindowState.Create
        self.window.set_title(self.WINDOW_TITLE + " *")
        self.txtFilterChain.set_text('<new>')
        self.change_state()

    def set_state_empty(self):
        self.state = WindowState.Empty
        self.window.set_title(self.WINDOW_TITLE)
        self.change_state()

    def set_state_modified(self):
        if self.state <> WindowState.Create:
            self.state = WindowState.Modified
            self.window.set_title(self.WINDOW_TITLE + " *")
            self.change_state()
                            
    def set_state_show(self):
        self.state = WindowState.Show
        self.window.set_title(self.WINDOW_TITLE)
        self.change_state()

    def show_config(self, filter):
        cls = map_filter_to_ui(filter)
        if cls is not None:
            win = cls(filter, self.filter_modif_callback)
            self.add_window_to_list(win)
            win.window.connect('destroy', self.on_window_destroy)
            win.window.show_all()
    
    def show_filter_chain(self):
        self.filterChainListStore.clear()
        for filter in self.fchain.filters:
            self.filterChainListStore.append(
                        [filter.__class__.__name__, filter.__doc__]) 

    def use_new_chain(self, chain):
        if chain is None:
            return
        for win in list(self.win_list):
            win.destroy()
        self.fchain = chain
        self.fchain.add_filter_observer(self.filters_changed_observer)
        self.show_filter_chain()
                                                                                    
    def on_btnNew_clicked(self, widget):
        if self.state == WindowState.Show:
            if self.msg_confirm_create_new() == Gtk.ResponseType.NO:
                return
        elif self.is_state_modified_or_created():
            result = self.msg_confirm_save_before_new()
            if result == Gtk.ResponseType.YES:
                pass
            elif result == Gtk.ResponseType.CANCEL:
                return
        self.use_new_chain(filterchain.FilterChain())
        self.set_state_create()

    def on_btnOpen_clicked(self, widget):
        if self.is_state_modified_or_created():
            result = self.msg_confirm_save_before_new()
            if result == Gtk.ResponseType.YES:
                pass
            elif result == Gtk.ResponseType.CANCEL:
                return

        dialog = Gtk.FileChooserDialog("Choose a filterchain file", None,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))
        ff = Gtk.FileFilter()
        ff.set_name('Filterchain')
        ff.add_pattern('*.filterchain')
    
        dialog.set_filter(ff)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            c = filterchain.read(dialog.get_filename())
            if c is not None:
                self.use_new_chain(c)
                self.txtFilterChain.set_text(dialog.get_filename())
                self.set_state_show()
        dialog.destroy()
            
    def on_btnSave_clicked(self, widget):
        self.save_chain()
        
    def on_btnSaveAs_clicked(self, widget):
        self.save_chain_as()

    def on_btnView_clicked(self, widget):
        win = WinViewer(self.fchain, self.server)
        win.window.connect('destroy', self.on_window_destroy)
        self.add_window_to_list(win)
        win.window.show_all()

    def on_btnAdd_clicked(self, widget):
        win = WinFilterSel()
        if win.window.run() == Gtk.ResponseType.OK:
            self.fchain.add_filter(win.selected_filter())
            self.set_state_modified()
        win.window.destroy()
            
    def on_btnRemove_clicked(self, widget):
        if (tree_row_selected(self.lstFilters) and 
                            self.msg_warn_del_row() == Gtk.ResponseType.YES):
            self.del_current_row()
                    
    def on_btnConfig_clicked(self, widget):
        if tree_row_selected(self.lstFilters):
            self.show_config(self.selected_filter())
                    
    def on_btnUp_clicked(self, widget):
        filter = self.selected_filter()
        if filter is not None:
            index = tree_selected_index(self.lstFilters)
            if index > 0:
                self.fchain.move_filter_up(filter)
                self.lstFilters.set_cursor(index - 1)
    
    def on_btnDown_clicked(self, widget):
        filter = self.selected_filter()
        if filter is not None:
            index = tree_selected_index(self.lstFilters)
            if index < len(self.fchain.filters) - 1:
                self.fchain.move_filter_down(filter)
                self.lstFilters.set_cursor(index + 1)
                    
    def on_btnTools_clicked(self, widget):
        self.menuTools.popup(None, None, None, None, 0, 
                             Gtk.get_current_event_time())

    def on_lstFilters_button_press_event(self, widget, event):
        if event.get_click_count()[1] == 2L:
            self.show_config(self.selected_filter())

    def on_window_destroy(self, widget):
        self.server.stop()
        self.win_list.remove(widget)

    def on_WinFilterChain_delete_event(self, widget, data=None):
        if self.is_state_modified_or_created():
            result = self.msg_confirm_save_before_closing()
            if result == Gtk.ResponseType.OK:
                if self.save_chain():
                    Gtk.main_quit()
            elif result == Gtk.ResponseType.CANCEL:
                return True
        self.server.stop()
        Gtk.main_quit()

    def on_toolLineMapper_activate(self, widget):
        win = WinMapper()
        self.add_window_to_list(win)
        win.window.connect('destroy', self.on_window_destroy)
        win.window.show_all()
        
    def on_toolLineTest_activate(self, widget):
        win = WinLineTest()
        self.add_window_to_list(win)
        win.window.connect('destroy', self.on_window_destroy)
        win.window.show_all()
    