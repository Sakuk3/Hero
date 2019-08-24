from core.file import File, File_manager
from gui.statusbar import Statusbar
from core.tab_manager import Tab_manager
import curses
import os

def main(stdscr):
    file_path = os.path.dirname(os.path.abspath(__file__))
    tab_manager = Tab_manager(os.path.dirname(os.path.abspath(__file__)))

    file_manager = File_manager()
    file_window = Statusbar(50,50,0,0,"sakuk","fff",file_path,tab_manager.tab_list)
    file_window.draw()

    file_window.refresh()

    stdscr.getkey()
    return
    stdscr.getkey()

    file_window.offset_x = 10
    file_viewer.draw()
    stdscr.getkey()

    file_window.offset_y = 10
    file_viewer.draw()
    stdscr.getkey()

    file_window.x = 10
    file_viewer.draw()
    stdscr.getkey()

    file_window.y = 10
    file_viewer.draw()
    stdscr.getkey()


curses.wrapper(main)
