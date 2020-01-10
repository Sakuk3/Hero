from gui.window import Window
import curses.textpad
class Editor(Window):
    def __init__(self,x,y,offset_x,offset_y,main_window,file):
        super().__init__(x,y,offset_x,offset_y,main_window)
        with open(file,'r') as f:
            self.file = list(f)

        self.textpad = textpad.Textbox(self.window).edit()
"""
        self.pos_x = 0
        self.pos_y = 0
        self.cursor_position = (0,0)

        self.draw()


    def draw(self):
        self.display_list(self.file)#[line[self.pos_y] for line in self.file[self.pos_x:self.x]])
        curses.setsyx(self.cursor_position[0],self.cursor_position[1])
        self.refresh()
        curses.setsyx(self.cursor_position[0],self.cursor_position[1])

    def keypress(self,key):
        self.draw()
        curses.wmove(self.cursor_position[0],self.cursor_position[1])
"""
