import os
class Tab:

    def __init__(self, path):
        self.index = [{'active':1,'path':path,'index':0}]

    def get_current_path(self):
        return (item for item in self.index if item["active"] == 1).__next__()['path']


    def set_current_path(self,new_path):
        self.index[[idx for idx,val in enumerate(self.index) if val["active"] == 1]]['active'] = 0

        if not any(item['path'] == new_path for item in self.index):
            self.index.append({'active':1,'path':new_path,'index':0})


    def get_selected_item_index(self):
        return (item for item in self.index if item["active"] == 1).__next__()['index']

    def set_selected_item_index(self,new_index):
        self.index[(idx for idx,item in enumerate(self.index) if item["active"] == 1).__next__()]['index'] = new_index
