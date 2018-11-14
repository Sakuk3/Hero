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
        window_parent_dir = curses.newwin(  curses.LINES-1-config.border_width,     round(config.parent_dir_width*curses.COLS/100),    config.border_width,  0)
    if config.current_dir_width != 0:
        window_current_dir = curses.newwin( curses.LINES-1-config.border_width,     round(config.current_dir_width*curses.COLS/100),   config.border_width,  round(config.parent_dir_width*curses.COLS/100)+config.border_width)
    if config.preview_width != 0:
        window_preview = curses.newwin(     curses.LINES-1-config.border_width,     round(config.preview_width*curses.COLS/100),       config.border_width,  round(config.parent_dir_width*curses.COLS/100)+round(config.current_dir_width*curses.COLS/100)+config.border_width)
    while True:
        selected_tab = [tab['tab'] for tab in tabs if tab['selected'] == True][0]
        stdscr.clear()
        window_parent_dir.clear()
        window_current_dir.clear()
        window_preview.clear()

        # display next path in top line
        if config.display_next_path:
            stdscr.addstr(0,0,str(selected_tab.selected_item_path),curses.A_REVERSE)

        # Draw tabs on top
        for idx,tab in enumerate(sorted(tabs,key=lambda x: int(x['index']))):
            if tab['selected'] == True:
                stdscr.addstr(0,curses.COLS-len(tabs)+idx,str(tab['index']),curses.A_REVERSE)
            else:
                stdscr.addstr(0,curses.COLS-len(tabs)+idx,str(tab['index']))

        # Draw contetns of the parent directory
        if config.parent_dir_width != 0 and selected_tab.path != '/':
            items = os.listdir(os.path.dirname(selected_tab.path))[:window_parent_dir.getmaxyx()[0]]
            for idx,entry in enumerate(items):
                window_parent_dir.addstr(idx,0,str(entry))

        # Draw contents of current directory
        if config.current_dir_width != 0:
            items = os.listdir(selected_tab.path)[:window_current_dir.getmaxyx()[0]]
            if(items):
                for index,entry in enumerate(items):
                    window_current_dir.addstr(index,0,str(entry))
                window_current_dir.chgat(selected_tab.selected_item_index, 0, curses.A_REVERSE)
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
            else:
                with open(selected_tab.selected_item_path) as f:
                    for i in range(window_preview.getmaxyx()[0]-1):
                        window_preview.addstr(i,0,f.readline()[:window_preview.getmaxyx()[1]])


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

        elif key in config.K_RIGHT:
            if(os.path.isdir(selected_tab.selected_item_path)):
                selected_tab.path = selected_tab.selected_item_path

        elif key in config.K_UP:
            selected_tab.selected_item_index -= 1

        elif key in config.K_DOWN:
            selected_tab.selected_item_index += 1

        elif(key in config.K_TABS):
            for tab in tabs:
                tab['selected'] = False
            if not any(tab.get('index', None) == int(key) for tab in tabs):
                tabs.append({'index':int(key),'tab':Tab(selected_tab.path),'selected':True})
            else:
                for tab in tabs:
                    if tab['index'] == int(key):
                        tab['selected'] = True

if __name__ == '__main__':
    curses.wrapper(main)
