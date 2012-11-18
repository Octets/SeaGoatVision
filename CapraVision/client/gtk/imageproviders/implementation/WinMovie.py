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

from gi.repository import Gtk, GObject

from CapraVision.client.gtk import get_ui
from CapraVision.client.gtk import win_name

from CapraVision.server.imageproviders.utils import supported_video_formats

class WinMovie:
    
    def __init__(self, source):
        self.source = source
        self.source.add_observer(self.source_observer)
        self.update_scale = True
        
        ui = get_ui(self, 'adjPosition')
        self.window = ui.get_object(win_name(self))
        self.adjPosition = ui.get_object('adjPosition')
        self.txtMovie = ui.get_object('txtMovie')
        self.lblTotal = ui.get_object('lblTotal')
        self.sclPosition = ui.get_object('sclPosition')
        self.spnWidth = ui.get_object('spnWidth')
        self.spnWidth.set_adjustment(self.create_adj_res())
        self.spnHeight = ui.get_object('spnHeight')
        self.spnHeight.set_adjustment(self.create_adj_res())
        self.spnFPS = ui.get_object('spnFPS')
        self.spnFPS.set_adjustment(self.create_adj_fps())
        
        if self.source.file_name == '':
            self.open_video()
        
    def create_adj_res(self):
        return Gtk.Adjustment(1, 1, 10000, 1, 10, 0)
        
    def create_adj_fps(self):
        return Gtk.Adjustment(1, 1, 255, 1, 10, 0)

    def open_video(self):
        dialog = Gtk.FileChooserDialog("Choose a video file", None,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK))
        ff = Gtk.FileFilter()
        ff.set_name("Videos")
        for imageformat in supported_video_formats():
            ff.add_pattern("*%(ext)s" % {"ext" : imageformat})
        dialog.set_filter(ff)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.txtMovie.set_text(dialog.get_filename())
            self.source.open_video_file(dialog.get_filename())
            
        dialog.destroy()
        
    def source_observer(self, source):
        GObject.idle_add(self.update_window)
        
    def update_window(self):
        if not self.source.is_opened():
            return
        
        fn = self.source.file_name
        if fn <> self.txtMovie.get_text():
            self.txtMovie.set_text(fn)
        
        total = self.source.get_total_frames()
        if str(total) <> self.lblTotal.get_text():
            self.lblTotal.set_text(str(int(total)))
        if total <> self.adjPosition.get_upper():
            self.adjPosition.set_upper(total)
            
        width = self.source.get_width()
        if width <> self.spnWidth.get_value():
            self.spnWidth.set_value(width)
            
        height = self.source.get_height()
        if height <> self.spnHeight.get_value():
            self.spnHeight.set_value(height)
        
        fps = self.source.get_fps()
        if fps <> self.spnFPS.get_value():
            self.spnFPS.set_value(fps)
            
        if self.update_scale:
            self.sclPosition.set_value(self.source.get_position())
        
    def on_btnOpen_clicked(self, widget):
        self.open_video()
        
    def on_btnPlay_clicked(self, widget):
        self.source.play()
    
    def on_btnPause_clicked(self, widget):
        self.source.pause()
        
    def on_sclPosition_button_press_event(self, widget, data):
        self.source.pause()

    def on_sclPosition_button_release_event(self, widget, data):
        self.source.set_position(int(self.sclPosition.get_value()))
        self.source.play()
        
    def on_spnWidth_value_changed(self, widget):
        self.source.set_width(self.spnWidth.get_value())
    
    def on_spnHeight_value_changed(self, widget):
        self.source.set_width(self.spnHeight.get_value())
    
    def on_spnFPS_value_changed(self, widget):
        self.source.set_fps(self.spnFPS.get_value())
    
    def on_WinMovie_destroy(self, widget):
        self.source.remove_observer(self.source_observer)
        