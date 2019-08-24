from gui.window import Window

class File_viewer(Window):
    def __init__(self,x,y,offset_x,offset_y,current_file,selected_file=None,show_size=False):
        super().__init__(x,y,offset_x,offset_y)
        self.current_file = current_file
        self.selected_file = selected_file
        self.show_size = show_size
        self.draw()

    def draw(self):
        self.clear(False)
        try:
            if self.current_file.is_dir:
                if len(self.current_file.content) == 0:
                    self.window.addstr(0,0,'empty',curses.color_pair(1))
                else:
                    for idx,entry in enumerate(self.current_file.content[:self.y]):
                        if self.show_size:
                            name = entry.full_name.ljust(self.y)[:-len(entry.size)]+entry.size
                        else:
                            name = entry.full_name.ljust(self.y)

                        if entry == self.selected_file:
                            self.add_str(idx,0,name,True)
                        else:
                            self.add_str(idx,0,name)
            else:
                try:
                    self.display_list(self.current_file.preview)
                except FileNotFoundError:
                    self.add_str(0,0,'ERROR')

        except PermissionError as e:
            self.add_str(0,0,'Permission Denied',curses.color_pair(1))

        self.refresh()
