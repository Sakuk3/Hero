import os
class Tab:

    def __init__(self, path):
        self._path = path

        if not os.listdir(self._path):
            self._selected_item_index = None
            self.selected_item_path = self._path
        else:
            self._selected_item_index = 0
            self.selected_item_path = os.path.join(self._path,os.listdir(self._path)[0])

        self._saved_paths = [{'path':path,'index':0}]

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._saved_paths.append({'path':self._path,'index':self._selected_item_index})
        #self.path = new_path
        self.selected_item_index = 0
        temp = self._saved_paths
        for idx,val in enumerate(self._saved_paths):
            if val['path'] == self.path:
                self.selected_item_index = val['index']
                self._saved_paths.pop(idx)
        if not os.listdir(self._path):
            self._selected_item_index = None
            self.selected_item_path = self._path
        else:
            self.selected_item_path = os.path.join(self._path,os.listdir(self._path)[self.selected_item_index])

    @property
    def selected_item_index(self):
        return self._selected_item_index

    @selected_item_index.setter
    def selected_item_index(self,value):
        # If directory is not empty
        if os.listdir(self._path):
            self._selected_item_index = value
            self.selected_item_path = os.path.join(self._path,os.listdir(self._path)[value])
