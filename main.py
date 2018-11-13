import curses
import os
import keymap
from tab import Tab

def main(stdscr):
    tabs = [None] * 10
    selected_tab = 0
    tabs[0] = Tab(os.path.dirname(os.path.abspath(__file__)))
    curses.curs_set(False)
    parent_dir_width    = 16
    current_dir_width   = 32
    preview_width       = 32
    parent_dir_hight    = curses.LINES-1
    current_dir_hight   = curses.LINES-1
    preview_hight       = curses.LINES-1
    border_width        = 1
    window_parent_dir = curses.newwin(  parent_dir_hight,   parent_dir_width,   1,  0)
    window_tabs = curses.newwin(        parent_dir_hight,   parent_dir_width,   1,  0)
    window_current_dir = curses.newwin( current_dir_hight,  current_dir_width,  1,  parent_dir_width+border_width)
    window_preview = curses.newwin(     preview_hight,      preview_width,      1,  current_dir_width+preview_width+border_width)
    # init colors
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    running = True
    while(running):
        draw_screen(stdscr,tabs,selected_tab,window_parent_dir,window_current_dir,window_preview)
        key = stdscr.getkey()
        if key in keymap.K_QUIT:
            running = False
        elif key in keymap.K_LEFT:
            if(tabs[selected_tab].get_current_path() != os.path.dirname(tabs[selected_tab].get_current_path())):
                tabs[selected_tab].set_current_path(os.path.dirname(tabs[selected_tab].get_current_path()))
                tabs[selected_tab].set_selected_item_index(0)
        elif key in keymap.K_RIGHT:
            if(os.listdir(tabs[selected_tab].get_current_path())[:1]):
                new_path = '/' +  os.listdir(tabs[selected_tab].get_current_path())[tabs[selected_tab].get_selected_item_index()]
                if(tabs[selected_tab].get_current_path() != '/'):
                    new_path = tabs[selected_tab].get_current_path() + new_path
                if(os.path.isdir(new_path) and os.access(new_path, os.R_OK)):
                    tabs[selected_tab].set_current_path(new_path)
                    tabs[selected_tab].set_selected_item_index(0)
        elif key in keymap.K_UP:
            if(tabs[selected_tab].get_selected_item_index() != 0):
                tabs[selected_tab].set_selected_item_index(tabs[selected_tab].get_selected_item_index() - 1)
        elif key in keymap.K_DOWN:
            if(tabs[selected_tab].get_selected_item_index() < len(os.listdir(tabs[selected_tab].get_current_path()))-1):
                tabs[selected_tab].set_selected_item_index(tabs[selected_tab].get_selected_item_index() + 1)
        elif(key in keymap.K_TABS):
            if tabs[int(key)] == None:
                tabs[int(key)] = Tab(os.path.dirname(os.path.abspath(__file__)))
            selected_tab = int(key)


def draw_screen(stdscr,tabs,selected_tab,window_parent_dir,window_current_dir,window_preview):
    stdscr.clear()

    # Draw current Path on top
    if(tabs[selected_tab].get_current_path() != '/'):
        stdscr.addstr(0,0,tabs[selected_tab].get_current_path()+'/'+os.listdir(tabs[selected_tab].get_current_path())[tabs[selected_tab].get_selected_item_index()],curses.A_REVERSE)
    else:
        stdscr.addstr(0,0,tabs[selected_tab].get_current_path()+os.listdir(tabs[selected_tab].get_current_path())[tabs[selected_tab].get_selected_item_index()],curses.A_REVERSE)

    stdscr.chgat(-1, curses.A_REVERSE)
    # display items from parent directory
    if(tabs[selected_tab].get_current_path() != '/'):
        items = os.listdir(os.path.dirname(tabs[selected_tab].get_current_path()))[:curses.LINES-1]
        for index,entry in enumerate(items):
            window_parent_dir.addstr(index,0,str(entry))


    # display items from current directory
    items = os.listdir(tabs[selected_tab].get_current_path())[:curses.LINES-1]
    if(items):
        for index,entry in enumerate(items):
            if(index != tabs[selected_tab].get_selected_item_index()):
                window_current_dir.addstr(index,0,str(entry))
            else:
                window_current_dir.addstr(index,0,str(entry),curses.A_REVERSE)
    else:
        window_current_dir.addstr(0,0,'empty',curses.color_pair(1))


    # display items from next directory
    if(items):
        new_path = '/' +  os.listdir(tabs[selected_tab].get_current_path())[tabs[selected_tab].get_selected_item_index()]
        if(tabs[selected_tab].get_current_path() != '/'):
            new_path = tabs[selected_tab].get_current_path() + new_path

        if(os.path.isdir(new_path)):
            items = None
            try:
                items = os.listdir(new_path)[:curses.LINES-1]
                if(items):
                    for index,entry in enumerate(items):
                        window_preview.addstr(index,0,str(entry))
                else:
                    window_preview.addstr(0,0,'empty',curses.color_pair(1))
            except PermissionError as e:
                window_preview.addstr(0,0,'Permission denied',curses.color_pair(1))

    # Draw tabs to screen
    number = sum(1 for i in tabs if i != None)
    for t in tabs:
        pass

    stdscr.refresh()
    window_current_dir.refresh()
    window_parent_dir.refresh()
    window_preview.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
