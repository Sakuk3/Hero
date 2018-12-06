import os

class tabs:
    def __init__(self,path):
        self.tabs = [tab(path,1)]

    def get_selected_tab(self):
        return [x for x in self.tabs if x.selected == True][0]
        


class tab:
    def __init__(self,path,index):
        self.path = path
        self.selected = True
        self.index = index
        self.selected_item = os.path.join(path,os.listdir(os.path.dirname(os.path.abspath(__file__)))[0])
