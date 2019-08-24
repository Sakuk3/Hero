from core.file import File, File_manager
from gui.file_viewer import File_viewer
import curses
import os

def main(stdscr):
    file_path = os.path.dirname(os.path.abspath(__file__))
    stdscr.getkey()
    file_manager = File_manager()
    file_window = File_viewer(50,50,0,0,file_manager.get_file(file_path))
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
