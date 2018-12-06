#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import os
import config
import subprocess
import shutil

def main(stdscr):
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    tabs = [{
        'index':1,
        'selected':True,
        'path':os.path.dirname(os.path.abspath(__file__)),
        'selected_item':os.path.join(os.path.dirname(os.path.abspath(__file__)),os.listdir(os.path.dirname(os.path.abspath(__file__)))[0])
    }]

    clipbord = ''

    # Create windows
    if config.parent_dir_width != 0:
        window_parent_dir = curses.newwin(  curses.LINES-10-config.border_width,     round(config.parent_dir_width*curses.COLS/100),    config.border_width,  0)
    if config.current_dir_width != 0:
        window_current_dir = curses.newwin( curses.LINES-10-config.border_width,     round(config.current_dir_width*curses.COLS/100),   config.border_width,  round(config.parent_dir_width*curses.COLS/100)+config.border_width)
    if config.preview_width != 0:
        window_preview = curses.newwin(     curses.LINES-10-config.border_width,     round(config.preview_width*curses.COLS/100),       config.border_width,  round(config.parent_dir_width*curses.COLS/100)+round(config.current_dir_width*curses.COLS/100)+config.border_width)

    window_path = curses.newwin(            1,                                      curses.COLS,                                       0,                     0)
    window_command = curses.newwin(         1,                                      curses.COLS,                                       curses.LINES-1,        0)

    while True:
        selected_tab = [tab for tab in tabs if tab['selected'] == True][0]
        window_path.clear()
        window_parent_dir.clear()
        window_current_dir.clear()
        window_preview.clear()

        # display next path in top line
        if config.display_next_path:
            window_path.addstr(0,0,str(selected_tab['path']),curses.A_REVERSE)


        # Draw tabs on top
        for idx,tab in enumerate(sorted(tabs,key=lambda x: int(x['index']))):
            if tab['selected'] == True:
                window_path.addstr(0,curses.COLS-1-len(tabs)+idx,str(tab['index']),curses.A_REVERSE)
            else:
                window_path.addstr(0,curses.COLS-1-len(tabs)+idx,str(tab['index']))


        # Draw contetns of the parent directory
        if config.parent_dir_width != 0 and selected_tab['path'] != '/':
            items = os.listdir(os.path.dirname(selected_tab['path']))[:window_parent_dir.getmaxyx()[0]]
            for idx,entry in enumerate(items):
                if entry == os.path.basename(selected_tab['path']):
                    window_parent_dir.addstr(idx,0,str(entry),curses.A_REVERSE)
                else:
                    window_parent_dir.addstr(idx,0,str(entry))

        # Draw contents of current directory
        if config.current_dir_width != 0:
            items = os.listdir(selected_tab['path'])[:window_current_dir.getmaxyx()[0]]
            if items :
                for index,entry in enumerate(items):
                    if entry == os.path.basename(selected_tab['selected_item']):
                        window_current_dir.addstr(index,0,str(entry),curses.A_REVERSE)
                    else:
                        window_current_dir.addstr(index,0,str(entry))
            else:
                window_current_dir.addstr(0,0,'empty',curses.color_pair(1))


        # Draw preview
        if config.preview_width != 0 and selected_tab['selected_item']:
            # preview for folders
            if os.path.isdir(selected_tab['selected_item']):
                try:
                    items = os.listdir(selected_tab['selected_item'])[:window_preview.getmaxyx()[0]]
                    if items:
                        for index,entry in enumerate(items):
                            window_preview.addstr(index,0,str(entry))
                    else:
                        window_preview.addstr(0,0,'empty',curses.color_pair(1))

                except PermissionError as e:
                    window_preview.addstr(0,0,'Permission denied',curses.color_pair(1))
            elif os.path.splitext(selected_tab['selected_item'])[1] in config.TXT_FILE_EXTENSIONS:
                with open(selected_tab['selected_item']) as f:
                    for i in range(window_preview.getmaxyx()[0]-1):
                        window_preview.addstr(i,0,f.readline()[:window_preview.getmaxyx()[1]])

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
            if selected_tab['path'] != '/':
                selected_tab['selected_item'] = selected_tab['path']
                selected_tab['path'] = os.path.dirname(selected_tab['path'])

        elif key in config.K_RIGHT:
            if selected_tab['selected_item']:
                if os.path.isdir(selected_tab['selected_item']):
                    selected_tab['path'] = selected_tab['selected_item']
                    if os.listdir(selected_tab['path']):
                        selected_tab['selected_item'] = os.path.join(selected_tab['path'],os.listdir(selected_tab['path'])[0])
                    else:
                        selected_tab['selected_item'] = None
                else:
                    # open file WIP
                    # curses.savetty()
                    # subprocess.run(['nano',selected_tab['selected_item']])
                    # curses.resetty()

                    # stdscr.keypad(True)
                    # curses.curs_set(False)
                    pass

        elif key in config.K_UP:
            if selected_tab['selected_item']:
                cur_index = os.listdir(selected_tab['path']).index(os.path.basename(selected_tab['selected_item']))
                if cur_index != 0:
                    selected_tab['selected_item'] = os.path.join(selected_tab['path'],os.listdir(selected_tab['path'])[cur_index-1])

        elif key in config.K_DOWN:
            if selected_tab['selected_item']:
                cur_index = os.listdir(selected_tab['path']).index(os.path.basename(selected_tab['selected_item']))
                if cur_index  < len(os.listdir(selected_tab['path']))-1:
                    selected_tab['selected_item'] = os.path.join(selected_tab['path'],os.listdir(selected_tab['path'])[cur_index+1])

        elif key in config.K_COPY:
            if selected_tab['selected_item']:
                clipbord = selected_tab['selected_item']
                window_command.addstr(0,0,'Copied to clipbord'.format(os.path.basename(selected_tab['selected_item'])),curses.A_REVERSE)
                window_command.refresh()

        elif key in config.K_PASTE:
            if clipbord != '':
                shutil.copy2(clipbord,selected_tab['path'])
                selected_tab['selected_item'] = os.path.join(selected_tab['path'],os.path.basename(clipbord))
                window_command.addstr(0,0,'Pasted',curses.A_REVERSE)
                window_command.refresh()

        elif key in config.K_DELETE:
            if selected_tab['selected_item']:
                cur_index = os.listdir(selected_tab['path']).index(os.path.basename(selected_tab['selected_item']))
                window_command.addstr(0,0,'Confirm deletion of {} (y/n)'.format(os.path.basename(selected_tab['selected_item'])),curses.A_REVERSE)
                window_command.refresh()
                key = stdscr.getkey()
                if key == 'y':
                    if os.path.isdir(selected_tab['selected_item']):
                        shutil.rmtree(selected_tab['selected_item'])
                    else:
                        os.remove(selected_tab['selected_item'])
                    if os.listdir(selected_tab['path']):
                        if cur_index != 0:
                            selected_tab['selected_item'] = os.path.join(selected_tab['path'],os.listdir(selected_tab['path'])[cur_index-1])
                        else:
                            selected_tab['selected_item'] = os.path.join(selected_tab['path'],os.listdir(selected_tab['path'])[0])
                    else:
                        selected_tab['selected_item'] = ''


        elif key in config.K_TABS:
            for tab in tabs:
                tab['selected'] = False
            if not any(tab.get('index', None) == int(key) for tab in tabs):
                tabs.append({
                    'index':1,
                    'selected':True,
                    'path':selected_tab['path'],
                    'selected_item':selected_tab['selected_item']
                    })


            else:
                for tab in tabs:
                    if tab['index'] == int(key):
                        tab['selected'] = True

if __name__ == '__main__':
    curses.wrapper(main)
