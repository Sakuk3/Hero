import curses
import shutil
import os

class actiones():

    def __init__(self):
        self.clipbord = None

    def copy(self,window_command,path):
        self.clipbord = path
        window_command.addstr(0,0,'Copied to clipbord',curses.A_REVERSE)
        window_command.refresh()

    def paste(self,window_command,path):
        if self.clipbord:
            if not os.path.exists(os.path.join(path,os.path.basename(self.clipbord))):
                shutil.copy2(self.clipbord,path)
                window_command.addstr(0,0,'Pasted',curses.A_REVERSE)
            else:
                window_command.addstr(0,0,'Item already exists',curses.A_REVERSE)
        window_command.addstr(0,0,'No path in clipbord',curses.A_REVERSE)
        window_command.refresh()

    def delete(self,window_command,path,stdscr):
        if path:
            window_command.addstr(0,0,'Confirm deletion of {} (y/n)'.format(os.path.basename(path)),curses.A_REVERSE)
            window_command.refresh()
            key = stdscr.getkey()
            if key == 'y':
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

    def create_folder(self,window_command,window_dir,path,stdscr):
        pass

    def create_file(self,window_command,window_dir,path,stdscr):
        pass

    def rename(self,window_command,window_dir,path,stdscr):
        pass
