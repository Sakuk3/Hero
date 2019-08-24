import curses

class Window():
    def __init__(self,x=0,y=0,offset_x=0,offset_y=0):
        self.window = curses.newwin(x,y,offset_x,offset_y)
        self.x = x
        self.y = y
        self.offset_x = offset_x
        self.offset_y = offset_y

    def add_str(self,y,x,string,hilighted=False,pad=False):
        string = str(string)
        if pad:
            string = string.ljust(self.y)
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
        self.window.refresh()

    def refresh(self):
        self.window.refresh()

    def display_list(self,content,hilighted=None):
        self.clear()
        if len(content) == 0:
            self.window.addstr(0,0,'empty',curses.color_pair(1))
        else:
            for idx,entry in enumerate(content[:self.y]):
                if idx == hilighted:
                    self.add_str(idx,0,entry,True,True)
                else:
                    self.add_str(idx,0,entry)
        self.refresh()

    def display_dir(self,content,hilighted=None):
        self.clear()
        if len(content) == 0:
            self.window.addstr(0,0,'empty',curses.color_pair(1))
        else:
            for idx,entry in enumerate(content[:self.y]):
                if entry.full_name == hilighted:
                    self.add_str(idx,0,entry.full_name.ljust(self.y-len(entry.size))+entry.size,True)
                else:
                    self.add_str(idx,0,entry.full_name.ljust(self.y-len(entry.size))+entry.size)
        self.refresh()
