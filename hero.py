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
import shutil

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
                self.tabs.selected_tab.selected_file_index -= 1
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_DOWN:
                self.tabs.selected_tab.selected_file_index += 1
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_LEFT:
                if self.tabs.selected_tab.selected_file.parent_dir:
                    self.tabs.selected_tab.current_file = self.tabs.selected_tab.current_file.parent_dir
                    self.render_topbar()
                    self.render_parent_directory()
                    self.render_current_directory()
                    self.render_preview()

            elif key in config.K_RIGHT:
                if self.tabs.selected_tab.selected_file.is_dir:
                    self.tabs.selected_tab.current_file = self.tabs.selected_tab.selected_file
                    self.render_topbar()
                    self.render_parent_directory()
                    self.render_current_directory()
                    self.render_preview()


            # Actiones
            elif key in config.K_RELOADE:
                self.render_topbar()
                self.render_parent_directory()
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_COPY:
                self.clipbord = self.tabs.selected_tab.selected_file
                self.windows["window_command"].add_str(0,0,'Copied to clipbord',True)
                self.windows["window_command"].refresh()

            elif key in config.K_PASTE:
                if self.clipbord:
                    if not os.path.exists(os.path.join(self.tabs.selected_tab.selected_file.path,self.clipbord.full_name)):
                        if os.path.exists(self.clipbord.path):
                            shutil.copy2(self.clipbord.path,self.tabs.selected_tab.current_file.path)
                            self.windows["window_command"].add_str(0,0,'Pasted',True)
                            #self.tabs.selected_tab.selected_file = self.tabs.selected_tab.selected_dir.index( os.path.basename(os.path.normpath(self.clipbord)))
                        else:
                            self.windows["window_command"].add_str(0,0,'Item no longer exists',True)
                            self.clipbord = None
                    else:
                        self.windows["window_command"].add_str(0,0,'Item already exists',True)
                else:
                        self.windows["window_command"].add_str(0,0,'No path in clipbord',True)
                self.windows["window_command"].refresh()
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_DELETE:
                # change selected item then deleate it
                if self.tabs.selected_tab.selected_file:
                    cur_index = self.tabs.selected_tab.selected_file_index
                    if cur_index > 0:
                        self.tabs.selected_tab.selected_file_index -=1
                    elif len(os.listdir(self.tabs.selected_tab.path)) == 1:
                        self.tabs.selected_tab.selected_file_index = None
                    else:
                        self.tabs.selected_tab.selected_file_index -=1

                    self.windows["window_command"].add_str(0,0,'Confirm deletion of {} (y/n)'.format(self.tabs.selected_tab.selected_file.full_name),True)
                    self.windows["window_command"].refresh()
                    key = self.stdscr.getkey()
                    if key == 'y':
                        if self.tabs.selected_tab.selected_file.is_dir:
                            shutil.rmtree(delete_path)
                        else:
                            os.remove(delete_path)

                        self.render_current_directory()
                        self.windows["window_command"].clear()
                        self.windows["window_command"].add_str(0,0,'Item deleated',True)
                        self.windows["window_command"].refresh()

                    else:
                        self.windows["window_command"].clear()

            elif key in config.K_RENAME:
                pass

            elif key in config.K_CREATE:
                pass

            self.windows["window_command"].add_str(0,0,str(self.tabs.selected_tab.selected_file.parent_dir),True)


    def render_parent_directory(self):
        # Draw contetns of the parent directory
        try:
            if self.tabs.selected_tab.current_file.parent_dir:
                self.windows["window_parent_dir"].display_dir(
                    self.tabs.selected_tab.current_file.parent_dir.content,
                    self.tabs.selected_tab.current_file.full_name)
            else:
                self.windows["window_parent_dir"].clear()
        except PermissionError as e:
            self.windows["window_parent_dir"].add_str(0,0,'Permission Denied',curses.color_pair(1))

    def render_current_directory(self):
        # Draw contents of current directory
        try:
            self.windows["window_current_dir"].display_dir(
                self.tabs.selected_tab.current_file.content,
                self.tabs.selected_tab.selected_file.full_name)
        except PermissionError as e:
            self.windows["window_current_dir"].add_str(0,0,'Permission Denied',True)

    def render_preview(self):
        self.windows["window_preview"].clear()
        # Draw preview
        if config.preview_width != 0 and isinstance(self.tabs.selected_tab.selected_file_index,int):
            # preview for folders
            if self.tabs.selected_tab.selected_file.is_dir:
                try:
                    self.windows["window_preview"].display_dir(self.tabs.selected_tab.selected_file.content)
                except PermissionError as e:
                    self.windows["window_preview"].add_str(0,0,'Permission Denied',curses.color_pair(1))


            elif self.tabs.selected_tab.selected_file.extension in config.TXT_FILE_EXTENSIONS:
                try:
                    self.windows["window_preview"].display_list(self.tabs.selected_tab.selected_file.preview,None)
                except FileNotFoundError:
                    self.windows["window_preview"].add_str(0,0,'ERROR')
        self.windows["window_preview"].refresh()

    def render_topbar(self):
        self.windows["window_topbar"].clear()

        if config.display_next_path:
            self.windows["window_topbar"].add_str(
                0,
                0,
                "{}@{} {}".format(
                getpass.getuser(),
                socket.gethostname(),
                self.tabs.selected_tab.current_file.path))

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
