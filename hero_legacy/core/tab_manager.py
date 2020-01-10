from core.file import File, File_manager
from core.tab import Tab

class Tab_manager:
    def __init__(self,path):
        self.file_manager = File_manager()
        self.tab_list = [Tab(self.file_manager.get_file(path),1,self.file_manager)]

    @property
    def selected_tab(self):
        return [x for x in self.tab_list if x.selected == True][0]

    def switch_tab(self,idx):
        temp_file = self.selected_tab.current_file
        self.selected_tab.selected = False
        if [x for x in self.tab_list if x.index == idx]:
            [x for x in self.tab_list if x.index == idx][0].selected = True
        else:
            self.tab_list.append(Tab(temp_file,idx,self.file_manager))
        self.tab_list.sort(key=lambda x: x.index)
