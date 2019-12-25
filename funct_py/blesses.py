import re
import sys 
import termios

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
    termios.tcsetattr(fd, termios.TCSADRAIN, new_terminal_state)
    return prev_terminal_state

def _restore_terminal(prev_terminal_state):
    sys.stdout.write(rmcup)
    sys.stdout.write(show_cursor)
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, prev_terminal_state)

def _move_cursor(row: int, col: int):
    sys.stdout.write("\x1b[{row};{col}H".format(row=row,col=col))

def write(row: int, col: int,string: str):
    _move_cursor(row,col)
    sys.stdout.write(string + "\n")

def get_size():
    pass

def wrapper(main: "main loop"):
    try:
        prev_terminal_state = _init_terminal()
        main()
    except Exception as e:
        print(e)
    finally:
        _restore_terminal(prev_terminal_state)
    
def demo():
    sys.stdin.read(1)
    write(0,0,"Hallo")
    sys.stdin.read(1)


if __name__ == '__main__':
    wrapper(demo)
