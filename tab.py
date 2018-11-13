import os
class Tab:

    def __init__(self, path):
        self.current_path = path
        self.selected_item_index = 0
        self.saved_paths = [{'path':path,'index':0}]

    def get_current_path(self):
        return self.current_path


    def set_current_path(self,new_path):
        self.saved_paths.append({'path':self.current_path,'index':self.selected_item_index})
        self.current_path = new_path
        self.selected_item_index = 0
        temp = self.saved_paths
        for idx,val in enumerate(self.saved_paths):
            if val['path'] == self.current_path:
                self.selected_item_index = val['index']
                self.saved_paths.pop(idx)



    def get_selected_item_index(self):
        return self.selected_item_index

    def set_selected_item_index(self,new_index):
        self.selected_item_index = new_index
