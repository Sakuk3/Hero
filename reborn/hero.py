#!/usr/bin/env python
# -*- coding: utf-8 -*-
from window import Window
from tabs import Tab,Tabs
import config
import actiones

import curses
import os

import socket
import getpass

class Hero():
    def __init__(self,stdscr):
        curses.curs_set(0)
        curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)

        self.clipbord = None
        self.tabs = Tabs(os.path.dirname(os.path.abspath(__file__)))
        self.windows = {}
        self.stdscr = stdscr

        self.windows["stdscr"] = Window(curses.LINES,curses.COLS,0,0)
        self.windows["stdscr"].window = self.stdscr

        if config.parent_dir_width != 0:
            self.windows["window_parent_dir"] = Window(
                curses.LINES-10-config.border_width,
                round(config.parent_dir_width*curses.COLS/100),#
                config.border_width,
                0)
        if config.current_dir_width != 0:
            self.windows["window_current_dir"] = Window(
                curses.LINES-10-config.border_width,
                round(config.current_dir_width*curses.COLS/100),
                config.border_width,
                round(config.parent_dir_width*curses.COLS/100)+config.border_width)
        if config.preview_width != 0:
            self.windows["window_preview"] = Window(
                curses.LINES-config.border_width,
                round(config.preview_width*curses.COLS/100),
                config.border_width,
                round(config.parent_dir_width*curses.COLS/100)+round(config.current_dir_width*curses.COLS/100)+config.border_width)

        self.windows["window_topbar"] = Window(1,curses.COLS,0,0)
        self.windows["window_command"] = Window(1,curses.COLS,curses.LINES-1,0)
        self.windows["window_info"] = Window(1,curses.COLS,curses.LINES-2,0)

        self.mainloop()

    def mainloop(self):
        self.clear_all_windows()
        self.refresh_all_windows()

        self.render_topbar()
        self.render_parent_directory()
        self.render_current_directory()
        self.render_preview()

        while True:
            # Get last keypress
            key = self.stdscr.getkey()
            self.windows["window_command"].clear()

            # End Programm
            if key in config.K_QUIT:
                curses.endwin()
                break

            elif key in config.K_TABS:
                self.tabs.switch_tab(int(key))

            elif key in config.K_UP:
                self.tabs.selected_tab.selected_item -= 1
                self.render_current_directory()
                self.render_preview()
            elif key in config.K_DOWN:
                self.tabs.selected_tab.selected_item += 1
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_LEFT:
                self.tabs.selected_tab.dir_back()

                self.render_topbar()
                self.render_parent_directory()
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_RIGHT:
                self.tabs.selected_tab.dir_next()

                self.render_topbar()
                self.render_parent_directory()
                self.render_current_directory()
                self.render_preview()

            # Actiones
            elif key in config.K_RELOADE:
                pass

    def render_parent_directory(self):
        # Draw contetns of the parent directory
        try:
            if self.tabs.selected_tab.path != '/':
                self.windows["window_parent_dir"].display_list(
                    self.tabs.selected_tab.parent_dir,
                    self.tabs.selected_tab.parent_dir.index(
                        os.path.basename(self.tabs.selected_tab.path)))
        except PermissionError as e:
            self.windows["window_parent_dir"].add_str(0,0,'Permission Denied',curses.color_pair(1))

    def render_current_directory(self):
        # Draw contents of current directory
        try:
            self.windows["window_current_dir"].display_list(
                self.tabs.selected_tab.dir,
                self.tabs.selected_tab.selected_item)
        except PermissionError as e:
            self.windows["window_current_dir"].add_str(0,0,'Permission Denied',True)

    def render_preview(self):
        # Draw preview
        if config.preview_width != 0 and isinstance(self.tabs.selected_tab.selected_item,int):
            # preview for folders
            if os.path.isdir(self.tabs.selected_tab.selected_item_path):
                try:
                    self.windows["window_preview"].display_list(self.tabs.selected_tab.selected_dir,None)
                except PermissionError as e:
                    self.windows["window_preview"].add_str(0,0,'Permission Denied',curses.color_pair(1))

            elif os.path.splitext(self.tabs.selected_tab.selected_item_name)[1] in config.TXT_FILE_EXTENSIONS:
                try:
                    with open(self.tabs.selected_tab.selected_item_path) as f:
                        content = []
                        for i in range(self.windows["window_preview"].y):
                            content.append(f.readline())
                        self.windows["window_preview"].display_list(content,None)
                except FileNotFoundError:
                    window_preview.addstr(0,0,'ERROR')

    def render_topbar(self):
        self.windows["window_topbar"].clear()

        if config.display_next_path:
            self.windows["window_topbar"].add_str(
                0,
                0,
                "{}@{} {}".format(
                getpass.getuser(),
                socket.gethostname(),
                self.tabs.selected_tab.path))

        for idx,tab in enumerate(self.tabs.tab_list):
            if tab.selected == True:
                self.windows["window_topbar"].add_str(
                    0,
                    curses.COLS-len(self.tabs.tab_list)+idx,
                    str(tab.index),
                    True)
            else:
                self.windows["window_topbar"].add_str(
                    0,
                    curses.COLS-len(self.tabs.tab_list)+idx,
                    str(tab.index))

        self.windows["window_topbar"].refresh()

    def clear_all_windows(self):
        for key,window in self.windows.items():
            window.clear()

    def refresh_all_windows(self):
        for key,window in self.windows.items():
            window.refresh()

    def init_colors(sefl):
        curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)

if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Hero(stdscr))
