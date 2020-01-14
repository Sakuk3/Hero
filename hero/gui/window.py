import curses

class Window():
    def __init__(self,x=0,y=0,offset_x=0,offset_y=0,main_window=None):
        if main_window:
            self.window = main_window.window.subwin(x,y,offset_x,offset_y)
            main_window.sub_windows.append(self)
        else:
            self.window = curses.newwin(x,y,offset_x,offset_y)

        self.sub_windows = []
        self._x = x
        self._y = y
        self._offset_x = offset_x
        self._offset_y = offset_y

    @property
    def x(self):
        return self.window.getmaxyx()[0]

    @x.setter
    def x(self, value):
        self.window.resize(self.x,self.y)

    @property
    def y(self):
        return self.window.getmaxyx()[1]

    @y.setter
    def y(self, value):
        self.window.resize(self.x,self.y)

    @property
    def offset_x(self):
        return self._offset_x

    @offset_x.setter
    def offset_x(self, value):
        self.clear(True)
        self._offset_x = value
        #del self.window
        #self.window = curses.newwin(self._x,self._y,self._offset_x,self._offset_y)
        self.window.mvwin(self._offset_x,self._offset_y)

    @property
    def offset_y(self):
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self.clear(True)
        self._offset_y = value
        #del self.window
        #self.window = curses.newwin(self._x,self._y,self._offset_x,self._offset_y)
        self.window.mvwin(self._offset_x,self._offset_y)


    def add_str(self,y,x,string,hilighted=False,pad=False):
        string = str(string)[:self.y-x]
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

    def clear(self,refresh=True):
        self.window.clear()
        if refresh:
            self.window.refresh()

    def refresh(self):
        self.window.refresh()

    def display_list(self,content,hilighted=None):
        self.clear()
        if content:
            if len(content) == 0:
                self.window.add_str(0,0,'empty')
            else:
                for idx,entry in enumerate(content[:self.x]):
                    if idx == hilighted:
                        self.add_str(idx,0,entry,True,True)
                    else:
                        self.add_str(idx,0,entry)
            self.refresh()
