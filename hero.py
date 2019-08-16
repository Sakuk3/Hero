#!/usr/bin/env python
# -*- coding: utf-8 -*-
from window import Window
from tabs import Tab,Tabs
import config

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


        self.windows["window_parent_dir"] = Window()
        self.windows["window_current_dir"] = Window()
        self.windows["window_preview"] = Window()
        self.windows["window_topbar"] = Window()
        self.windows["window_command"] = Window()
        self.windows["window_info"] = Window()

        self.resize()

        self.mainloop()

    def resize(self):
        self.windows["window_parent_dir"] = Window(
            curses.LINES-3,
            round(config.parent_dir_width*curses.COLS/100),
            1,
            0)

        self.windows["window_current_dir"] = Window(
            curses.LINES-3,
            round(config.current_dir_width*curses.COLS/100),
            1,
            self.windows["window_parent_dir"].y+1)

        self.windows["window_preview"] = Window(
            curses.LINES,
            curses.COLS - (self.windows["window_current_dir"].y+self.windows["window_current_dir"].offset_y+1),
            1,
            self.windows["window_current_dir"].y+self.windows["window_current_dir"].offset_y+1)

        self.windows["window_topbar"] = Window(1,curses.COLS,0,0)
        self.windows["window_command"] = Window(1,curses.COLS,curses.LINES-1,0)
        self.windows["window_info"] = Window(1,curses.COLS,curses.LINES-2,0)
        self.redraw()

    def mainloop(self):
        self.clear_all_windows()
        self.refresh_all_windows()

        self.render_topbar()
        self.render_parent_directory()
        self.render_current_directory()
        self.render_preview()

        while True:
            # Get last keypress
            key = self.get_next_keypress()
            self.windows["window_command"].clear()

            # End Programm
            if key in config.K_QUIT:
                curses.endwin()
                break

            elif key in config.K_TABS:
                self.tabs.switch_tab(int(key))
                self.redraw()

            elif key in config.K_UP:
                self.tabs.selected_tab.selected_file_index -= 1
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_DOWN:
                self.tabs.selected_tab.selected_file_index += 1
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_LEFT:
                if self.tabs.selected_tab.current_file.parent_dir:
                    self.tabs.selected_tab.current_file = self.tabs.selected_tab.current_file.parent_dir
                    self.redraw()

            elif key in config.K_RIGHT:
                if self.tabs.selected_tab.selected_file:
                    if self.tabs.selected_tab.selected_file.is_dir:
                        self.tabs.selected_tab.current_file = self.tabs.selected_tab.selected_file
                        self.redraw()


            # Actiones
            elif key in config.K_RELOADE:
                self.redraw()

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
                    if self.tabs.selected_tab.selected_file_index > 0:
                        self.tabs.selected_tab.selected_file_index -=1

                    if len(self.tabs.selected_tab.current_file.content) == 1:
                        self.tabs.selected_tab.selected_file_index = None


                    self.windows["window_command"].add_str(0,0,'Confirm deletion of {} (y/n)'.format(self.tabs.selected_tab.selected_file.full_name),True)
                    self.windows["window_command"].refresh()
                    key = self.get_next_keypress()
                    if key == 'y':
                        if self.tabs.selected_tab.selected_file.is_dir:
                            shutil.rmtree(self.tabs.selected_tab.selected_file.path)
                        else:
                            os.remove(self.tabs.selected_tab.selected_file.path)

                        self.render_current_directory()
                        self.render_preview()
                        self.render_parent_directory()

                        self.windows["window_command"].clear()
                        self.windows["window_command"].add_str(0,0,'Item deleated',True)
                        self.windows["window_command"].refresh()

                    else:
                        self.windows["window_command"].clear()

            elif key in config.K_RENAME:
                pass

            elif key in config.K_CREATE:
                pass

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
            if self.tabs.selected_tab.current_file.content:
                self.windows["window_current_dir"].display_dir(
                    self.tabs.selected_tab.current_file.content,
                    self.tabs.selected_tab.selected_file.full_name,
                    True)
            else:
                self.windows["window_current_dir"].add_str(0,0,'empty',True)
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


            elif self.tabs.selected_tab.selected_file.preview:
                try:
                    self.windows["window_preview"].display_list(self.tabs.selected_tab.selected_file.preview,None)
                except FileNotFoundError:
                    self.windows["window_preview"].add_str(0,0,'ERROR')
        self.windows["window_preview"].refresh()

    def render_topbar(self):
        self.windows["window_topbar"].clear()

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

    def redraw(self):
        self.clear_all_windows()
        self.render_topbar()
        self.render_parent_directory()
        self.render_current_directory()
        self.render_preview()

    def get_next_keypress(self):
        while True:
            keypress = self.stdscr.getkey()
            if keypress == curses.KEY_RESIZE:
                self.resize()
            else:
                return keypress

if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Hero(stdscr))
