from gui.window import Window

"""
    Displays list of string lifo
"""
class console(Window):
    def __init__(self,x,y,offset_x,offset_y,main_window=None):
        super().__init__(x,y,offset_x,offset_y,main_window)
        self._strings = []
        self.draw()

    def add_string(self,string):
        self._strings.append(string)
        if len(self._strings) > self.x:
            self._strings.pop(0)

    def draw(self):
        self.clear(False)
        self.display_list(self._strings)
        self.refresh()
