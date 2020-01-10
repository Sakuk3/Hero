import re
import sys 
import termios
import tty
import os

# reference http://xn--rpa.cc/irl/term.html
smcup = "\x1b[?1049h" # switches to alternative buffering
clear = "\x1b[2J"     # hard clear
rmcup = "\x1b[?1049l" # restore terminal
hide_cursor = "\x1b[?25l"
show_cursor = "\x1b[?25h"

# 7-bit C1 ANSI sequences
ansi_escape = re.compile(r'''
    \x1B    # ESC
    [@-_]   # 7-bit C1 Fe
    [0-?]*  # Parameter bytes
    [ -/]*  # Intermediate bytes
    [@-~]   # Final byte
''', re.VERBOSE)

def _init_terminal():
    sys.stdout.write(smcup+clear+hide_cursor+"\n")
    
    fd = sys.stdin.fileno()
    prev_terminal_state = termios.tcgetattr(fd)
    new_terminal_state = termios.tcgetattr(fd)
    new_terminal_state[3] = new_terminal_state[3] & ~termios.ECHO & ~termios.ICANON         # lflags
    tty.setcbreak(fd, when=termios.TCSAFLUSH)
    termios.tcsetattr(fd, termios.TCSADRAIN, new_terminal_state)
    return prev_terminal_state

def _restore_terminal(prev_terminal_state):
    sys.stdout.write(rmcup)
    sys.stdout.write(show_cursor)
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, prev_terminal_state)

def _move_cursor(row: int, col: int):
    sys.stdout.write("\x1b[{row};{col}H".format(row=row+1,col=col))

def clear_terminal():
    sys.stdout.write(clear + "\n")

def add_str(row: int, col: int,string: str):
    _move_cursor(row,col)
    sys.stdout.write(str(string)  + "\n")

def get_max_row_col():
    return reversed(os.get_terminal_size())

def get_key():
    key = sys.stdin.read(1)
    if key == "\x1b":
        key = sys.stdin.read(2)
    return key

def display_list(
    height: int, 
    width: int, 
    width_offset: int, 
    height_offset: int, 
    list, 
    selected_item=None,
    list_offsset=0):

    list = [str(idx)+": "+e for idx,e in enumerate(list)]
    for idx,entry in enumerate(list[list_offsset:height+list_offsset-1]):
        if entry == selected_item:
            add_str(height_offset+idx,width_offset,inverse(entry))
        else:
            add_str(height_offset+idx,width_offset,entry)


def inverse(string: str):
    return "\x1b[7m"+str(string)+"\x1b[0m"

def strip_esc(string: str):
    return ansi_escape.sub('', string)

"""
    Initiates the terminal for curses like use.
    Calls function
    Restores terminal to original state
"""
def wrapper(funct: "function to execute"):
    error = None
    try:
        prev_terminal_state = _init_terminal()
        funct()
    except Exception as e:
        error = e
    finally:
        _restore_terminal(prev_terminal_state)
        if error: 
            print(error)
  
def demo():
    while True:
        add_str(0,0,str(get_key()))


if __name__ == '__main__':
    wrapper(demo)
