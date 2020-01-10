from core.file import File, File_manager
from gui.file_viewer import File_viewer
import curses
import os

def main(stdscr):
    curses.curs_set(0)
    stdscr.refresh()

    file_path = os.path.dirname(os.path.abspath(__file__))
    file_manager = File_manager()
    test = File_viewer(10,10,0,0,file_manager.get_file(file_path))

    stdscr.getkey()

    test.offset_x = 10
    test.draw()
    stdscr.getkey()

    test.offset_y = 10
    test.draw()
    stdscr.getkey()

    test.x = 10
    test.draw()
    stdscr.getkey()

    test.y = 10
    test.draw()
    stdscr.getkey()


curses.wrapper(main)
