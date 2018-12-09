import os

class tabs:
    def __init__(self,path):
        self.tab_list = [tab(path,1)]

    def get_selected_tab(self):
        return [x for x in self.tab_list if x.selected == True][0]

    def switch_tab(self,idx):
        temp_path = self.get_selected_tab().path
        self.get_selected_tab().selected = False
        if [x for x in self.tab_list if x.index == idx]:
            [x for x in self.tab_list if x.index == idx][0].selected = True
        else:
            self.tab_list.append(tab(temp_path,idx))
        self.tab_list.sort(key=lambda x: x.index)

class tab:
    def __init__(self,path,index):
        self.path = path
        self.selected = True
        self.index = index
        self.selected_item = os.path.join(path,os.listdir(os.path.dirname(os.path.abspath(__file__)))[0])

    def list_current_dir(self):
        return os.listdir(self.path)

    def list_parent_dir(self):
        return os.listdir(os.path.dirname(self.path))

    def list_selected_dir(self):
        if os.path.isdir(self.selected_item):
            return os.listdir(self.selected_item)
        else:
            return[]

    def dir_back(self):
        if self.path != '':
            self.selected_item = self.path
            self.path = os.path.dirname(self.path)

    def dir_next(self):
        if self.selected_item and os.path.isdir(self.selected_item):
            self.path = self.selected_item
            if os.listdir(self.path):
                self.selected_item = os.path.join(self.path,os.listdir(self.path)[0])
            else:
                self.selected_item = False

    def idx_up(self):
        if self.selected_item:
            cur_index = os.listdir(self.path).index(os.path.basename(self.selected_item))
            if cur_index != 0:
                self.selected_item = os.path.join(self.path,os.listdir(self.path)[cur_index-1])

    def idx_down(self):
        if self.selected_item:
            cur_index = os.listdir(self.path).index(os.path.basename(self.selected_item))
            if cur_index  < len(os.listdir(self.path))-1:
                self.selected_item = os.path.join(self.path,os.listdir(self.path)[cur_index+1])



class ftp_tab(tab):
    def __init__(self,path,index):
        super().__init__()
        self.path = path
        self.selected = True
        self.index = index
        self.selected_item = os.path.join(path,os.listdir(os.path.dirname(os.path.abspath(__file__)))[0])

    def list_current_dir(self):
        return os.listdir(self.path)

    def list_parent_dir(self):
        return os.listdir(os.path.dirname(self.path))

    def list_selected_dir(self):
        if os.path.isdir(self.selected_item):
            return os.listdir(self.selected_item)
        else:
            return[]

    def dir_back(self):
        if self.path != '':
            self.selected_item = self.path
            self.path = os.path.dirname(self.path)

    def dir_next(self):
        if self.selected_item and os.path.isdir(self.selected_item):
            self.path = self.selected_item
            if os.listdir(self.path):
                self.selected_item = os.path.join(self.path,os.listdir(self.path)[0])
            else:
                self.selected_item = False

    def idx_up(self):
        if self.selected_item:
            cur_index = os.listdir(self.path).index(os.path.basename(self.selected_item))
            if cur_index != 0:
                self.selected_item = os.path.join(self.path,os.listdir(self.path)[cur_index-1])

    def idx_down(self):
        if self.selected_item:
            cur_index = os.listdir(self.path).index(os.path.basename(self.selected_item))
            if cur_index  < len(os.listdir(self.path))-1:
                self.selected_item = os.path.join(self.path,os.listdir(self.path)[cur_index+1])
