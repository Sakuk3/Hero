import curses

class Window():
    def __init__(self,x=0,y=0,offset_x=0,offset_y=0):
        self.window = curses.newwin(x,y,offset_x,offset_y)
        self._offset_x = offset_x
        self._offset_y = offset_y

    @property
    def x(self):
        return self.window.getmaxyx()[0]

    @x.setter
    def x(self, value):
        self.window.resize(self._x,self._y)

    @property
    def y(self):
        return self.window.getmaxyx()[1]

    @y.setter
    def y(self, value):
        self.window.resize(self._x,self._y)

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
        if len(content) == 0:
            self.window.addstr(0,0,'empty',curses.color_pair(1))
        else:
            for idx,entry in enumerate(content[:self.y]):
                if idx == hilighted:
                    self.add_str(idx,0,entry,True,True)
                else:
                    self.add_str(idx,0,entry)
        self.refresh()
