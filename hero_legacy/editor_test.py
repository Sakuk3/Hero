from gui.editor import Editor
import curses
import os

def main(stdscr):
    file_path = "hero.py"
    editor = Editor(50,100,0,0,None,file_path)
    editor.draw()
    stdscr.refresh()
    editor.textpad.edit()

    while True:
        key = stdscr.getkey()
        if key == "+":
            break
        else:
            editor.keypress(key)


curses.wrapper(main)
