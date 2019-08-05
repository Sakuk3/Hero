import os

class Tabs:
    def __init__(self,path):
        self.tab_list = [Tab(path,1)]

    @property
    def selected_tab(self):
        return [x for x in self.tab_list if x.selected == True][0]

    def switch_tab(self,idx):
        temp_path = self.selected_tab.path
        self.selected_tab.selected = False
        if [x for x in self.tab_list if x.index == idx]:
            [x for x in self.tab_list if x.index == idx][0].selected = True
        else:
            self.tab_list.append(Tab(temp_path,idx))
        self.tab_list.sort(key=lambda x: x.index)

class Tab:
    def __init__(self,path,index):
        self.path = path
        self.selected = True
        self.index = index
        self.selected_item = 0

    @property
    def selected_item_path(self):
        if len(os.listdir(os.path.dirname(self.path))) != 0:
            return os.path.join(self.path,self.dir[self.selected_item])
        else:
            return None

    @property
    def dir(self):
        return os.listdir(self.path)

    @property
    def parent_dir(self):
        return os.listdir(os.path.dirname(self.path))

    @property
    def selected_dir(self):
        if os.path.isdir(self.selected_item_path):
            return os.listdir(self.selected_item_path)
        else:
            return []
    @property
    def selected_item(self):
        return self._selected_item

    @property
    def selected_item_name(self):
        if isinstance(self.selected_item, int):
            return self.dir[self.selected_item]
        else:
            return None

    @selected_item.setter
    def selected_item(self, value):
        if os.listdir(os.path.dirname(self.path)) == []:
            self._selected_item = None
        elif value < 0:
            self._selected_item = 0
        elif value > len(os.listdir(self.path))-1:
            self._selected_item = len(os.listdir(self.path))-1
        else:
            self._selected_item = value

    def dir_back(self):
        if self.path != '/':
            self.selected_item = self.parent_dir.index(
                os.path.basename(self.path))
            self.path = os.path.dirname(self.path)

    def dir_next(self):
        try:
            if self.selected_item and os.path.isdir(self.selected_item_path):
                self.path = os.path.join(self.path,self.dir[self.selected_item])
                self.selected_item = 0
        except PermissionError as e:
            pass
