import re
import sys
import termios
import tty
import os
import traceback

# reference http://xn--rpa.cc/irl/term.html
smcup = "\x1b[?1049h"  # switches to alternative buffering
clear = "\x1b[2J"     # hard clear
rmcup = "\x1b[?1049l"  # restore terminal
hide_cursor = "\x1b[?25l"
show_cursor = "\x1b[?25h"

# 7-bit C1 ANSI sequences
ansi_escape_regex = r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'


def _init_terminal():
    sys.stdout.write(smcup+clear+hide_cursor+"\n")

    fd = sys.stdin.fileno()
    prev_terminal_state = termios.tcgetattr(fd)
    new_terminal_state = termios.tcgetattr(fd)
    # lflags
    new_terminal_state[3] = new_terminal_state[3] & ~termios.ECHO & ~termios.ICANON
    tty.setcbreak(fd, when=termios.TCSAFLUSH)
    termios.tcsetattr(fd, termios.TCSADRAIN, new_terminal_state)
    return prev_terminal_state


def _restore_terminal(prev_terminal_state):
    sys.stdout.write(rmcup)
    sys.stdout.write(show_cursor)
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, prev_terminal_state)


def _move_cursor(row: int, col: int):
    sys.stdout.write("\x1b[{row};{col}H".format(row=row+1, col=col))


def clear_terminal():
    sys.stdout.write(clear + "\n")


def add_str(row: int, col: int, string: str):
    _move_cursor(row, col)
    sys.stdout.write(str(string) + "\x1b[0m")


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
    height_offset: int,
    width_offset: int,
    list: list,
    selected_item: str = None,
    list_offsset: int = 0,
    line_numbers: bool = False
):
    if line_numbers:
        line_number_length = 4
        list = [(str(idx)+": ").rjust(line_number_length)+e for idx, e in enumerate(list)]
        width -= line_number_length

    for idx, entry in enumerate(list[list_offsset:height+list_offsset-1]):
        if entry == selected_item:
            add_str(height_offset+idx, width_offset, inverse(shorten_str_disp(entry,width)))
        else:
            add_str(height_offset+idx, width_offset, shorten_str_disp(entry,width))


def draw():
    sys.stdout.write("\n")


def inverse(string: str):
    return "\x1b[7m"+str(string)+"\x1b[0m"


# strip ansi escape sequences from string
def strip_esc(string: str):
    return re.sub(ansi_escape_regex,'',string)


# shorten the string while ignoring all ansi escape sequences
def shorten_str_disp(string: str,len: int):
    return string[:len]
    return_str = ""
    counter = 0
    for element in re.split("(" + ansi_escape_regex + ")",string):
        if element.startswith(r'\x1b'):
            return_str += element
            counter +=1
        else:
            for char in element:
                return_str += char
                counter += 1
                if counter >= len:
                    break

    return return_str+"\x1b[0m"


def display_box(
    height: int,
    width: int,
    width_offset: int,
    height_offset: int,):
    box_borders = {
        "topLeft": "╔",
        "topRight": "╗",
        "bottomRight": "╝",
        "bottomLeft": "╚",
        "vertical": "║",
        "horizontal": "═"
    }
    # Top Line
    add_str(
        height_offset,
        width_offset,
        box_borders["topLeft"]+box_borders["horizontal"] *
        (width-2)+box_borders["topRight"]
    )
    add_str(
        height_offset+height,
        width_offset,
        box_borders["bottomLeft"]+box_borders["horizontal"] *
        (width-2)+box_borders["bottomRight"]
    )
    for line_index in range(height-2):
        add_str(
            height_offset+line_index,
            width_offset,
            box_borders["vertical"]
        )
        add_str(
            height_offset+line_index,
            width_offset+width,
            box_borders["vertical"]
        )


"""
    Initiates the terminal for curses like use.
    Calls function
    Restores terminal to original state
"""


def wrapper(funct: "function to execute"):
    try:
        prev_terminal_state = _init_terminal()
        funct()
    finally:
        _restore_terminal(prev_terminal_state)


def demo():
    while True:
        add_str(0, 0, str(get_key()))


if __name__ == '__main__':
    wrapper(demo)
