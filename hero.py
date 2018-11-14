import curses
import os
import config
from tab import Tab

def main(stdscr):
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    tabs = [{'index':1,'selected':True,'tab':Tab(os.path.dirname(os.path.abspath(__file__)))}]

    # Create windows
    if config.parent_dir_width != 0:
        window_parent_dir = curses.newwin(  curses.LINES-1-config.border_width,     config.parent_dir_width,    config.border_width,  0)
    if config.current_dir_width != 0:
        window_current_dir = curses.newwin( curses.LINES-1-config.border_width,     config.current_dir_width,   config.border_width,  config.parent_dir_width+config.border_width)
    if config.preview_width != 0:
        window_preview = curses.newwin(     curses.LINES-1-config.border_width,     config.preview_width,       config.border_width,  config.current_dir_width+config.preview_width+config.border_width)
    while True:
        selected_tab = [tab['tab'] for tab in tabs if tab['selected'] == True][0]

        # display next path in top line
        if config.display_next_path:
            stdscr.addstr(0,0,str(selected_tab.selected_item_path),curses.A_REVERSE)

        # Draw tabs on top
        for tab in tabs:
            if tab['selected'] == True:
                stdscr.addstr(0,curses.COLS-len(tabs)+int(tab['index']) - 1,str(tab['index']),curses.A_REVERSE)
            else:
                stdscr.addstr(0,curses.COLS-len(tabs)+int(tab['index']) -1,str(tab['index']))

        # Draw contetns of the parent directory
        if config.parent_dir_width != 0 and selected_tab.path != '/':
            items = os.listdir(os.path.dirname(selected_tab.path))[:window_parent_dir.getmaxyx()[0]]
            for idx,entry in enumerate(items):
                window_parent_dir.addstr(idx,0,str(entry))

        # Draw contents of current directory
        if config.parent_dir_width != 0:
            items = os.listdir(selected_tab.path)[:window_current_dir.getmaxyx()[0]]
            if(items):
                for index,entry in enumerate(items):
                    if(index != selected_tab.selected_item_index):
                        window_current_dir.addstr(index,0,str(entry))
                    else:
                        window_current_dir.addstr(index,0,str(entry),curses.A_REVERSE)
            else:
                window_current_dir.addstr(0,0,'empty',curses.color_pair(1))

        # Draw preview
        if config.preview_width != 0:
            # preview for folders
            if(os.path.isdir(selected_tab.selected_item_path)):
                try:
                    items = os.listdir(selected_tab.selected_item_path)[:window_preview.getmaxyx()[0]]
                    if(items):
                        for index,entry in enumerate(items):
                            window_preview.addstr(index,0,str(entry))
                    else:
                        window_preview.addstr(0,0,'empty',curses.color_pair(1))
                except PermissionError as e:
                    window_preview.addstr(0,0,'Permission denied',curses.color_pair(1))


        # Reload windows
        stdscr.refresh()
        window_current_dir.refresh()
        window_parent_dir.refresh()
        window_preview.refresh()

        key = stdscr.getkey()
        if key in config.K_QUIT:
            break
        elif key in config.K_LEFT:
            selected_tab.path = os.path.dirname(selected_tab.path)
            """
        elif key in keymap.K_RIGHT:
            if(os.listdir(tabs[selected_tab].get_current_path())[:1]):
                new_path = '/' +  os.listdir(tabs[selected_tab].get_current_path())[tabs[selected_tab].get_selected_item_index()]
                if(tabs[selected_tab].get_current_path() != '/'):
                    new_path = tabs[selected_tab].get_current_path() + new_path
                if(os.path.isdir(new_path) and os.access(new_path, os.R_OK)):
                    tabs[selected_tab].set_current_path(new_path)
        elif key in keymap.K_UP:
            if(tabs[selected_tab].get_selected_item_index() != 0):
                tabs[selected_tab].set_selected_item_index(tabs[selected_tab].get_selected_item_index() - 1)
        elif key in keymap.K_DOWN:
            if(tabs[selected_tab].get_selected_item_index() < len(os.listdir(tabs[selected_tab].get_current_path()))-1):
                tabs[selected_tab].set_selected_item_index(tabs[selected_tab].get_selected_item_index() + 1)
        elif(key in keymap.K_TABS):
            if tabs[int(key)-1] == None:
                tabs[int(key)-1] = Tab(os.path.dirname(os.path.abspath(__file__)))
                tabs = sorted(tabs, key=lambda k: k['index'])
            selected_tab = int(key)-1
        """

if __name__ == '__main__':
    curses.wrapper(main)
