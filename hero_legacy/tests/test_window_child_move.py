import curses
from gui.window_child import Window_child

def main(stdscr):
    curses.curs_set(0)
    stdscr.refresh()

    test = Window_child(3,3,0,0)

    stdscr.getkey()

    test.offset_x = 10
    test.draw()
    stdscr.getkey()

    test.offset_y = 10
    test.draw()
    stdscr.getkey()

    test.x = 30
    test.draw()
    stdscr.getkey()

    test.y = 30
    test.draw()
    stdscr.getkey()

curses.wrapper(main)
