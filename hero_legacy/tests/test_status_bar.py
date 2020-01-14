from core.file import File, File_manager
from gui.statusbar import Statusbar
from core.tab_manager import Tab_manager
import curses
import os

def main(stdscr):
    curses.curs_set(0)
    stdscr.refresh()

    file_path = os.path.dirname(os.path.abspath(__file__))
    tab_manager = Tab_manager(os.path.dirname(os.path.abspath(__file__)))
    file_manager = File_manager()

    test = Statusbar(1,10,0,0,"sakuk","fff",file_path,tab_manager.tab_list)

    stdscr.getkey()

    test.offset_x = 10
    test.draw()
    stdscr.getkey()

    test.offset_y = 10
    test.draw()
    stdscr.getkey()

    test.x = 1
    test.draw()
    stdscr.getkey()

    test.y = 50
    test.draw()
    stdscr.getkey()


curses.wrapper(main)
