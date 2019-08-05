#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import os
import config

class Window():
    def __init__(self,x,y,offset_x,offset_y):
        self.window = curses.newwin(x,y,offset_x,offset_y)
        self.x = x
        self.y = y
        self.offset_x = offset_x
        self.offset_y = offset_y

    def add_str(self,y,x,string,hilighted=False):
        string = str(string)
        try:
            if hilighted:
                self.window.addstr(y,x,string,curses.A_REVERSE)
            else:
                self.window.addstr(y,x,string)
            self.refresh()
        except:
            pass



    def clear(self):
        self.window.clear()

    def refresh(self):
        self.window.refresh()

    def display_list(self,content,hilighted=0):
        self.clear()
        if len(content) == 0:
            self.window.addstr(0,0,'empty',curses.color_pair(1))
        else:
            for idx,entry in enumerate(content[:self.y]):
                if idx == hilighted:
                    self.add_str(idx,0,entry,True)
                else:
                    self.add_str(idx,0,entry)
        self.refresh()

class Tabs:
    def __init__(self,path):
        self.tab_list = [Tab(path,1)]

    @property
    def selected_tab(self):
        return [x for x in self.tab_list if x.selected == True][0]

    def switch_tab(self,idx):
        temp_path = self.selected_tab.path
        self.selected_tab.selected = False
        if [x for x in self.tab_list if x.index == idx]:
            [x for x in self.tab_list if x.index == idx][0].selected = True
        else:
            self.tab_list.append(Tab(temp_path,idx))
        self.tab_list.sort(key=lambda x: x.index)

class Tab:
    def __init__(self,path,index):
        self.path = path
        self.selected = True
        self.index = index
        self.selected_item = 0

    @property
    def selected_item_path(self):
        if len(os.listdir(os.path.dirname(self.path))) != 0:
            return os.path.join(self.path,self.dir[self.selected_item])
        else:
            return None

    @property
    def dir(self):
        return os.listdir(self.path)

    @property
    def parent_dir(self):
        return os.listdir(os.path.dirname(self.path))

    @property
    def selected_dir(self):
        if os.path.isdir(self.selected_item_path):
            return os.listdir(self.selected_item_path)
        else:
            return []
    @property
    def selected_item(self):
        return self._selected_item

    @property
    def selected_item_name(self):
        if self.selected_item:
            return self.dir[self.selected_item]
        else:
            return None

    @selected_item.setter
    def selected_item(self, value):
        if os.listdir(os.path.dirname(self.path)) == []:
            self._selected_item = None
        elif value < 0:
            self._selected_item = 0
        elif value > len(os.listdir(self.path))-1:
            self._selected_item = len(os.listdir(self.path))-1
        else:
            self._selected_item = value

    def dir_back(self):
        if self.path != '/':
            self.selected_item = self.parent_dir.index(
                os.path.basename(self.path))
            self.path = os.path.dirname(self.path)

    def dir_next(self):
        try:
            if self.selected_item and os.path.isdir(self.selected_item_path):
                self.path = os.path.join(self.path,self.dir[self.selected_item])
                self.selected_item = 0
        except PermissionError as e:
            pass

def main(stdscr):
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    stdscr_window = Window(curses.LINES,curses.COLS,0,0)
    stdscr_window.window = stdscr
    clipbord = None

    windows = {"stdscrv":stdscr_window}

    tabs = Tabs(os.path.dirname(os.path.abspath(__file__)))


    if config.parent_dir_width != 0:
        windows["window_parent_dir"] = Window(
            curses.LINES-10-config.border_width,
            round(config.parent_dir_width*curses.COLS/100),#
            config.border_width,
            0)
    if config.current_dir_width != 0:
        windows["window_current_dir"] = Window(
            curses.LINES-10-config.border_width,
            round(config.current_dir_width*curses.COLS/100),
            config.border_width,
            round(config.parent_dir_width*curses.COLS/100)+config.border_width)
    if config.preview_width != 0:
        windows["window_preview"] = Window(
            curses.LINES-config.border_width,
            round(config.preview_width*curses.COLS/100),
            config.border_width,
            round(config.parent_dir_width*curses.COLS/100)+round(config.current_dir_width*curses.COLS/100)+config.border_width)

    windows["window_path"] = Window(1,curses.COLS,0,0)
    windows["window_command"] = Window(1,curses.COLS,curses.LINES-1,0)
    windows["window_info"] = Window(1,curses.COLS,curses.LINES-2,0)
    for key,window in windows.items():
        window.clear()
    # Main Loop
    while True:
        windows["window_path"].clear()
        # display next path in top line
        if config.display_next_path:
            windows["window_path"].add_str(
                0,
                0,
                tabs.selected_tab.path,
                True)

        # Draw tabs on top
        for idx,tab in enumerate(tabs.tab_list):
            if tab.selected == True:
                windows["window_path"].add_str(
                    0,
                    curses.COLS-1-len(tabs.tab_list)+idx,
                    str(tab.index),
                    True)
            else:
                windows["window_path"].add_str(
                    0,
                    curses.COLS-1-len(tabs.tab_list)+idx,
                    str(tab.index))

        # Draw contetns of the parent directory
        try:
            if tabs.selected_tab.path != '/':
                windows["window_parent_dir"].display_list(
                    tabs.selected_tab.parent_dir,
                    tabs.selected_tab.parent_dir.index(
                        os.path.basename(tabs.selected_tab.path)))
        except PermissionError as e:
            windows["window_parent_dir"].add_str(0,0,'Permission Denied',curses.color_pair(1))


        # Draw contents of current directory
        try:
            windows["window_current_dir"].display_list(
                tabs.selected_tab.dir,
                tabs.selected_tab.selected_item)
        except PermissionError as e:
            windows["window_current_dir"].add_str(0,0,'Permission Denied',True)

        # Draw preview
        if config.preview_width != 0 and tabs.selected_tab.selected_item:
            # preview for folders
            if os.path.isdir(tabs.selected_tab.selected_item_path):
                try:
                    windows["window_preview"].display_list(tabs.selected_tab.selected_dir,None)
                except PermissionError as e:
                    windows["window_preview"].add_str(0,0,'Permission Denied',curses.color_pair(1))

            elif os.path.splitext(tabs.selected_tab.selected_item_name)[1] in config.TXT_FILE_EXTENSIONS:
                try:
                    with open(tabs.selected_tab.selected_item_path) as f:
                        content = []
                        for i in range(windows["window_preview"].y):
                            content.append(f.readline())
                        windows["window_preview"].display_list(content,None)
                except FileNotFoundError:
                    window_preview.addstr(0,0,'ERROR')

        # Get last keypress
        key = stdscr.getkey()
        windows["window_command"].clear()


        # End Programm
        if key in config.K_QUIT:
            curses.endwin()
            break

        elif key in config.K_TABS:
            tabs.switch_tab(int(key))

        elif key in config.K_UP:
            tabs.selected_tab.selected_item -= 1

        elif key in config.K_DOWN:
            tabs.selected_tab.selected_item += 1

        elif key in config.K_LEFT:
            tabs.selected_tab.dir_back()

        elif key in config.K_RIGHT:
            tabs.selected_tab.dir_next()

        # Actiones
        elif key in config.K_RELOADE:
            pass

        elif key in config.K_COPY:
            clipbord = tabs.selected_tab.path
            windows["window_command"].add_str(0,0,'Copied to clipbord',True)
            windows["window_command"].refresh()
        elif key in config.K_PASTE:
            if clipbord:
                actiones.paste(tabs.get_selected_tab().path)
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

if __name__ == '__main__':
    curses.wrapper(main)
