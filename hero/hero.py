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

        self.stdscr.refresh()
        self.parent_dir_widged = File_viewer(
            self.stdscr.x-3,
            round(config.parent_dir_width*self.stdscr.y/100),
            1,
            0,
            self.tab_manager.selected_tab.current_file.parent_dir,self.tab_manager.selected_tab.current_file)

        self.current_dir_widged = File_viewer(
            self.stdscr.x-3,
            round(config.current_dir_width*self.stdscr.y/100),
            1,
            self.parent_dir_widged.y,
            self.tab_manager.selected_tab.current_file,self.tab_manager.selected_tab.selected_file,True)

        self.preview_widged = File_viewer(
            self.stdscr.x-3,
            self.stdscr.y-self.parent_dir_widged.y-self.current_dir_widged.y-1,
            1,
            self.stdscr.y-(self.stdscr.y-self.parent_dir_widged.y-self.current_dir_widged.y-1),
            self.tab_manager.selected_tab.selected_file)

        self.statusbar = Statusbar(
            1,
            self.stdscr.y,
            0,
            0,
            getpass.getuser(),socket.gethostname(),self.tab_manager.selected_tab.current_file.path,self.tab_manager.tab_list)

        self.window_command = Window(
            1,
            self.stdscr.y,
            self.stdscr.x-1,
            0)

        self.window_info = Window(
            1,
            self.stdscr.y,
            self.stdscr.x-2,
            0)

        self.stdscr.refresh()


        #self.resize()
        self.stdscr.refresh()
        self.mainloop()

    def resize(self):
        self.parent_dir_widged.x = self.stdscr.x-3
        self.parent_dir_widged.y = round(config.parent_dir_width*self.stdscr.y/100)

        self.current_dir_widged.x = self.stdscr.x-3
        self.current_dir_widged.y = round(config.current_dir_width*self.stdscr.y/100)
        self.current_dir_widged.offset_y = self.parent_dir_widged.y

        self.preview_widged.x = self.stdscr.x-3
        self.preview_widged.y = self.stdscr.y-self.parent_dir_widged.y-self.current_dir_widged.y-1
        self.preview_widged.offset_y = self.stdscr.y-(self.stdscr.y-self.parent_dir_widged.y-self.current_dir_widged.y-1)

        self.window_command.y = self.stdscr.y
        self.window_command.offset_x = self.stdscr.x-1

        self.window_info.y = self.stdscr.y
        self.window_info.offset_x = self.stdscr.x-2

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

            elif key in [str(i) for i in range(1,10)]:
                self.tab_manager.switch_tab(int(key))
                self.statusbar.tab_list = self.tab_manager.tab_list
                self.statusbar.path = self.tab_manager.selected_tab.current_file.path
                self.statusbar.draw()


                self.parent_dir_widged.current_file = self.tab_manager.selected_tab.current_file.parent_dir
                self.parent_dir_widged.selected_file = self.tab_manager.selected_tab.current_file
                self.parent_dir_widged.draw()

                self.current_dir_widged.current_file = self.tab_manager.selected_tab.current_file
                self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                self.current_dir_widged.draw()

                self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                self.preview_widged.draw()

            elif key in config.K_UP:
                self.tab_manager.selected_tab.selected_file_index -= 1
                self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                self.current_dir_widged.draw()

                self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                self.preview_widged.draw()

            elif key in config.K_DOWN:
                self.tab_manager.selected_tab.selected_file_index += 1

                self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                self.current_dir_widged.draw()

                self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                self.preview_widged.draw()

            elif key in config.K_LEFT:
                if self.tab_manager.selected_tab.current_file.parent_dir:
                    self.tab_manager.selected_tab.current_file = self.tab_manager.selected_tab.current_file.parent_dir

                    self.parent_dir_widged.current_file = self.tab_manager.selected_tab.current_file.parent_dir
                    self.parent_dir_widged.selected_file = self.tab_manager.selected_tab.current_file
                    self.parent_dir_widged.draw()

                    self.current_dir_widged.current_file = self.tab_manager.selected_tab.current_file
                    self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                    self.current_dir_widged.draw()

                    self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                    self.preview_widged.draw()

            elif key in config.K_RIGHT:
                if self.tab_manager.selected_tab.selected_file:
                    if self.tab_manager.selected_tab.selected_file.is_dir:
                        self.tab_manager.selected_tab.current_file = self.tab_manager.selected_tab.selected_file

                        self.parent_dir_widged.current_file = self.tab_manager.selected_tab.current_file.parent_dir
                        self.parent_dir_widged.selected_file = self.tab_manager.selected_tab.current_file
                        self.parent_dir_widged.draw()

                        self.current_dir_widged.current_file = self.tab_manager.selected_tab.current_file
                        self.current_dir_widged.selected_file = self.tab_manager.selected_tab.selected_file
                        self.current_dir_widged.draw()

                        self.preview_widged.current_file = self.tab_manager.selected_tab.selected_file
                        self.preview_widged.draw()


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
        self.window_info.add_str(0,0,self.stdscr.y)
        self.parent_dir_widged.draw()
        self.current_dir_widged.draw()
        self.preview_widged.draw()
        self.statusbar.draw()
        self.window_command.refresh()
        self.window_info.refresh()
        self.stdscr.refresh()

    def get_next_keypress(self):
        while True:
            keypress = self.stdscr.window.getkey()

            if keypress == "KEY_RESIZE":
                pass
                #self.resize()
            else:
                return keypress

if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Hero(stdscr))
