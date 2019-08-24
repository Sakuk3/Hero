#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui.window import Window
from gui.statusbar import Statusbar
from gui.file_viewer import File_viewer

from core.tab_manager import Tab_manager
import config.config as config

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
        self.tab_manager = Tab_manager(os.path.dirname(os.path.abspath(__file__)))
        self.stdscr = Window(curses.LINES,curses.COLS,0,0)
        self.stdscr.window = stdscr


        self.parent_dir_widged = File_viewer(0,0,0,0,self.tab_manager.selected_tab.current_file.parent_dir,self.tab_manager.selected_tab.current_file)
        self.current_dir_widged = File_viewer(0,0,0,0,self.tab_manager.selected_tab.current_file,self.tab_manager.selected_tab.selected_file,True)
        self.preview_widged = File_viewer(0,0,0,0,self.tab_manager.selected_tab.selected_file)
        self.statusbar = Statusbar(0,0,0,0,getpass.getuser(),socket.gethostname(),self.tab_manager.selected_tab.current_file.path,self.tab_manager.tab_list)
        self.window_command = Window()
        self.window_info = Window()

        self.resize()
        self.mainloop()

    def resize(self):
        self.parent_dir_widged.x = curses.LINES-3
        self.parent_dir_widged.y = round(config.parent_dir_width*curses.COLS/100)
        self.parent_dir_widged.offset_x = 1
        self.parent_dir_widged.offset_y = 0

        self.current_dir_widged.x = curses.LINES-3
        self.current_dir_widged.y = round(config.current_dir_width*curses.COLS/100)
        self.current_dir_widged.offset_x = 1
        self.current_dir_widged.offset_y = self.parent_dir_widged.y+1

        self.preview_widged.x = curses.LINES-1
        self.preview_widged.y = round(config.parent_dir_width*curses.COLS/100)
        self.preview_widged.offset_x = 1
        self.preview_widged.offset_y = curses.COLS - (self.current_dir_widged.y+self.current_dir_widged.offset_y+1)

        self.statusbar.x = 1
        self.statusbar.y = curses.COLS
        self.statusbar.offset_x = 0
        self.statusbar.offset_y = 0

        self.window_command.x = 1
        self.window_command.y = curses.COLS
        self.window_command.offset_x = curses.LINES-1
        self.window_command.offset_y = 0

        self.window_info.x = 1
        self.window_info.y = curses.COLS
        self.window_info.offset_x = curses.LINES-2
        self.window_info.offset_y = 0

        self.redraw()

    def mainloop(self):

        while True:
            # Get last keypress
            key = self.get_next_keypress()
            self.window_command.clear()

            # End Programm
            if key in config.K_QUIT:
                curses.endwin()
                break

            elif key in range(1,10):
                self.tab_manager.switch_tab(int(key))
                self.redraw()

            elif key in config.K_UP:
                self.tab_manager.selected_tab.selected_file_index -= 1
                self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                self.current_dir_widged.refresh()

                self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                self.preview_widged.refresh()

            elif key in config.K_DOWN:
                self.tab_manager.selected_tab.selected_file_index += 1

                self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                self.current_dir_widged.refresh()

                self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                self.preview_widged.refresh()

            elif key in config.K_LEFT:
                if self.tab_manager.selected_tab.current_file.parent_dir:
                    self.parent_dir_widged.current_file = self.tab_manager.selected_tab.selected_file.parent_dir
                    self.parent_dir_widged.selected_file = self.tab_manager.selected_tab.current_file
                    self.parent_dir_widged.refresh()

                    self.current_dir_widged.current_file = self.tab_manager.selected_tab.current_file
                    self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                    self.current_dir_widged.refresh()

                    self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                    self.preview_widged.refresh()

            elif key in config.K_RIGHT:
                if self.tab_manager.selected_tab.selected_file:
                    if self.tab_manager.selected_tab.selected_file.is_dir:
                        self.parent_dir_widged.current_file = self.tab_manager.selected_tab.selected_file.parent_dir
                        self.parent_dir_widged.selected_file = self.tab_manager.selected_tab.current_file
                        self.parent_dir_widged.refresh()

                        self.current_dir_widged.current_file = self.tab_manager.selected_tab.current_file
                        self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                        self.current_dir_widged.refresh()

                        self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                        self.preview_widged.refresh()


            # Actiones
            elif key in config.K_RELOADE:
                self.redraw()

            elif key in config.K_COPY:
                if self.tab_manager.selected_tab.selected_file:
                    self.clipbord = self.tab_manager.selected_tab.selected_file
                    self.window_command.add_str(0,0,'Copied to clipbord',True)
                    self.window_command.refresh()
                else:
                    self.window_command.add_str(0,0,'No location selected',True)
                    self.window_command.refresh()

            elif key in config.K_PASTE:
                if self.clipbord:
                    if not os.path.exists(os.path.join(self.tab_manager.selected_tab.selected_file.path,self.clipbord.full_name)):
                        if os.path.exists(self.clipbord.path):
                            shutil.copy2(self.clipbord.path,self.tab_manager.selected_tab.current_file.path)
                            self.window_command.add_str(0,0,'Pasted',True)
                            #self.tab_manager.selected_tab.selected_file = self.tab_manager.selected_tab.selected_dir.index( os.path.basename(os.path.normpath(self.clipbord)))
                        else:
                            self.window_command.add_str(0,0,'Item no longer exists',True)
                            self.clipbord = None
                    else:
                        self.window_command.add_str(0,0,'Item already exists',True)
                else:
                        self.window_command.add_str(0,0,'No path in clipbord',True)
                self.window_command.refresh()
                self.render_current_directory()
                self.render_preview()

            elif key in config.K_DELETE:
                # change selected item then deleate it
                if self.tab_manager.selected_tab.selected_file:
                    if self.tab_manager.selected_tab.selected_file_index > 0:
                        self.tab_manager.selected_tab.selected_file_index -=1

                    if len(self.tab_manager.selected_tab.current_file.content) == 1:
                        self.tab_manager.selected_tab.selected_file_index = None


                    self.window_command.add_str(0,0,'Confirm deletion of {} (y/n)'.format(self.tab_manager.selected_tab.selected_file.full_name),True)
                    self.window_command.refresh()
                    key = self.get_next_keypress()
                    if key == 'y':
                        if self.tab_manager.selected_tab.selected_file.is_dir:
                            shutil.rmtree(self.tab_manager.selected_tab.selected_file.path)
                        else:
                            os.remove(self.tab_manager.selected_tab.selected_file.path)

                        self.render_current_directory()
                        self.render_preview()
                        self.render_parent_directory()

                        self.window_command.clear()
                        self.window_command.add_str(0,0,'Item deleated',True)
                        self.window_command.refresh()

                    else:
                        self.window_command.clear()

            elif key in config.K_RENAME:
                pass

            elif key in config.K_CREATE:
                pass

    def init_colors(sefl):
        curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    def redraw(self):
        self.parent_dir_widged.refresh()
        self.current_dir_widged.refresh()
        self.preview_widged.refresh()
        self.statusbar.refresh()
        self.window_command.refresh()
        self.window_info.refresh()

    def get_next_keypress(self):
        while True:
            keypress = self.stdscr.window.getkey()
            if keypress == curses.KEY_RESIZE:
                self.resize()
            else:
                return keypress

if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Hero(stdscr))
