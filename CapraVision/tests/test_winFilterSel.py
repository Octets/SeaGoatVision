import os
os.chdir(os.path.join(os.getcwd(), ".."))
os.sys.path.insert(0,os.getcwd()) 

from gi.repository import Gtk

from gui.gui import WinFilterSel

if __name__ == '__main__':
    win = WinFilterSel()
    win.window.show_all()
    Gtk.main()