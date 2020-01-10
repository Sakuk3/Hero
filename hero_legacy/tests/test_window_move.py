import curses
from gui.window import Window


def main(stdscr):
    test = Window(10,10,0,0)

    stdscr.getkey()

    for i in range(test.y):
        test.add_str(i,0,"+"*test.x)

    test.refresh()

    stdscr.getkey()
    test.clear()
    test.offset_x = 15
    test.clear()
    for i in range(test.y):
        test.add_str(i,0,"+"*test.x)
    test.refresh()

    stdscr.getkey()

curses.wrapper(main)
