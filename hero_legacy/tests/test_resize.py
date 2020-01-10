import curses
from gui.window import Window


def main(stdscr):
    test = Window(30,30,0,0)
    while True:
        test.clear()
        test.add_str(0,0,"Lines: {} Colums: {}".format(curses.LINES,curses.COLS))
        test.add_str(1,0,"{}".format(stdscr.getmaxyx()))
        stdscr.getkey()

curses.wrapper(main)
