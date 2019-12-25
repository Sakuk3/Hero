import curses
import os
import socket
import getpass

from models import Model, Tab, File
from render import Render
from eventHandler import EventHandler
from modelHandler import init_model

def main(stdscr):
    curses.curs_set(0)
    model = init_model(
        os.path.dirname(os.path.abspath(__file__)),
        getpass.getuser(),
        socket.gethostname()
        )

    while not model.exit:
        Render(model,stdscr)
        model = EventHandler(model,stdscr.getkey())

if __name__ == '__main__':
    curses.wrapper(main)
