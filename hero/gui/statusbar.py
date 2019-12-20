from gui.window import Window

class Statusbar(Window):
    def __init__(self,x,y,offset_x,offset_y,main_window,username,hostname,path,tab_list):
        super().__init__(x,y,offset_x,offset_y,main_window)
        self.username = username
        self.hostname = hostname
        self.path = path
        self.tab_list = tab_list
        self.draw()

    def draw(self):
        self.clear(False)

        self.add_str(
            0,
            0,
            "{}@{} {}".format(
                self.username,
                self.hostname,
                self.path))

        for idx,tab in enumerate(self.tab_list):
            if tab.selected == True:
                self.add_str(
                    0,
                    self.y-len(self.tab_list)+idx,
                    str(tab.index),
                    True)
            else:
                self.add_str(
                    0,
                    self.y-len(self.tab_list)+idx,
                    str(tab.index))

        self.refresh()
