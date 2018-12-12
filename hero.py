#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import os
import config
import subprocess


from actiones import actiones as act
from tabs import tabs as t

def main(stdscr):
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    tabs = t(os.path.dirname(os.path.abspath(__file__)))
    actiones = act()

    # Create windows
    if config.parent_dir_width != 0:
        window_parent_dir = curses.newwin(  curses.LINES-10-config.border_width,     round(config.parent_dir_width*curses.COLS/100),    config.border_width,  0)
    if config.current_dir_width != 0:
        window_current_dir = curses.newwin( curses.LINES-10-config.border_width,     round(config.current_dir_width*curses.COLS/100),   config.border_width,  round(config.parent_dir_width*curses.COLS/100)+config.border_width)
    if config.preview_width != 0:
        window_preview = curses.newwin(     curses.LINES-10-config.border_width,     round(config.preview_width*curses.COLS/100),       config.border_width,  round(config.parent_dir_width*curses.COLS/100)+round(config.current_dir_width*curses.COLS/100)+config.border_width)

    window_path = curses.newwin(            1,                                      curses.COLS,                                       0,                     0)
    window_command = curses.newwin(         1,                                      curses.COLS,                                       curses.LINES-1,        0)
    window_info = curses.newwin(            1,                                      curses.COLS,                                       curses.LINES-2,        0)


    while True:
        window_path.clear()
        window_parent_dir.clear()
        window_current_dir.clear()
        window_preview.clear()

        # display next path in top line
        if config.display_next_path:
            window_path.addstr(0,0,os.stat(tabs.get_selected_tab().selected_item),curses.A_REVERSE)


        # Draw tabs on top
        for idx,tab in enumerate(tabs.tab_list):
            if tab.selected == True:
                window_path.addstr(0,curses.COLS-1-len(tabs.tab_list)+idx,str(tab.index),curses.A_REVERSE)
            else:
                window_path.addstr(0,curses.COLS-1-len(tabs.tab_list)+idx,str(tab.index))

        # Display File/Filder Info
        if tabs.get_selected_tab().selected_item:
            window_info.addstr(0,curses.COLS-1-len(tabs.tab_list)+idx,str(tab.index),curses.A_REVERSE)


        # Draw contetns of the parent directory
        if config.parent_dir_width != 0 and tabs.get_selected_tab().path != '/':
            try:
                list_directory(window_parent_dir,tabs.get_selected_tab().list_parent_dir(),os.path.basename(tabs.get_selected_tab().path))
            except PermissionError as e:
                window_parent_dir.addstr(0,0,'Permission Denied',curses.color_pair(1))

        # Draw contents of current directory
        if config.current_dir_width != 0:
            try:
                if tabs.get_selected_tab().selected_item:
                    list_directory(window_current_dir,tabs.get_selected_tab().list_current_dir(),os.path.basename(tabs.get_selected_tab().selected_item))
                else:
                    list_directory(window_current_dir,tabs.get_selected_tab().list_current_dir())
            except PermissionError as e:
                window_current_dir.addstr(0,0,'Permission Denied',curses.color_pair(1))

        # Draw preview
        if config.preview_width != 0 and tabs.get_selected_tab().selected_item:
            # preview for folders
            if os.path.isdir(tabs.get_selected_tab().selected_item):
                try:
                    list_directory(window_preview,tabs.get_selected_tab().list_selected_dir())
                except PermissionError as e:
                    window_preview.addstr(0,0,'Permission Denied',curses.color_pair(1))

            elif os.path.splitext(tabs.get_selected_tab().selected_item)[1] in config.TXT_FILE_EXTENSIONS:
                try:
                    with open(tabs.get_selected_tab().selected_item) as f:
                        for i in range(window_preview.getmaxyx()[0]-1):
                            window_preview.addstr(i,0,f.readline()[:window_preview.getmaxyx()[1]])
                except FileNotFoundError:
                    window_preview.addstr(0,0,'ERROR')

        # Reload windows
        stdscr.refresh()
        window_path.refresh()
        window_current_dir.refresh()
        window_parent_dir.refresh()
        window_preview.refresh()

        key = stdscr.getkey()

        window_command.clear()
        window_command.refresh()

        if key in config.K_QUIT:
            curses.endwin()
            break

        elif key in config.K_LEFT:
            tabs.get_selected_tab().dir_back()

        elif key in config.K_RIGHT:
            tabs.get_selected_tab().dir_next()

        elif key in config.K_UP:
            tabs.get_selected_tab().idx_up()

        elif key in config.K_DOWN:
            tabs.get_selected_tab().idx_down()

        elif key in config.K_TABS:
            tabs.switch_tab(int(key))

        # Actiones
        elif key in config.K_RELOADE:
            pass

        elif key in config.K_COPY:
            actiones.copy(window_command,tabs.get_selected_tab().selected_item)

        elif key in config.K_PASTE:
            if actiones.clipbord:
                actiones.paste(window_command,tabs.get_selected_tab().path)
                tabs.get_selected_tab().selected_item = actiones.clipbord

        elif key in config.K_DELETE:
            # change selected item then deleate it
            cur_index = os.listdir(tabs.get_selected_tab().path).index(os.path.basename(tabs.get_selected_tab().selected_item))
            delete_path = tabs.get_selected_tab().selected_item
            if cur_index > 0:
                tabs.get_selected_tab().idx_up()
            elif len(os.listdir(tabs.get_selected_tab().path)) == 1:
                tabs.get_selected_tab().selected_item = None
            else:
                tabs.get_selected_tab().idx_up


            actiones.delete(window_command,delete_path,stdscr)

        elif key in config.K_RENAME:
            pass
        elif key in config.K_CREATE:
            pass


"""
    window:     The Window to draw on
    content:    A list of the contets of the directory to draw
    hilighted:  The entry to hilight
"""
def list_directory(window,content,hilighted=None):
    if len(content) == 0:
        window.addstr(0,0,'empty',curses.color_pair(1))
    if len(content) > 0:
        for idx,entry in enumerate(content[:window.getmaxyx()[0]]):
            if entry == hilighted:
                window.addstr(idx,0,str(entry),curses.A_REVERSE)
            else:
                window.addstr(idx,0,str(entry))




if __name__ == '__main__':
    curses.wrapper(main)
