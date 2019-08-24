import curses
from gui.window_child import Window_child


def main(stdscr):
    #stdscr.getkey()

    test = Window_child(10,10,0,0)
    stdscr.refresh()
    stdscr.getkey()

    test.clear()
    test.offset_x = 15
    test.draw()
    stdscr.getkey()

curses.wrapper(main)
