from gui.window import Window

class Window_child(Window):
    def __init__(self,x,y,offset_x,offset_y):
        super().__init__(x,y,offset_x,offset_y)
        self.draw()

    def draw(self):
        self.clear(False)
        for i in range(self.x):
            self.add_str(i,0,"+"*self.y)
        self.refresh()
