import os
from core.file import File, File_manager

class Tab:
    def __init__(self,current_file,index,file_manager):
        self._current_file = current_file
        self.selected = True
        self.index = index
        self.file_manager = file_manager

        if self._current_file.content:
            self._selected_file_index = 0
        else:
            self._selected_file_index = None

    @property
    def current_file(self):
        return self._current_file


    @current_file.setter
    def current_file(self, value):
        if value:
            if value == self._current_file.parent_dir:
                self._selected_file_index = [file.full_name for file in self._current_file.parent_dir.content].index(self._current_file.full_name)
                self._current_file = value
            else:
                self._current_file = value
                self.selected_file_index = 0

    @property
    def selected_file(self):
        if self._selected_file_index == None:
            return None
        else:
            return self._current_file.content[self._selected_file_index]

    @property
    def selected_file_index(self):
        return self._selected_file_index

    @selected_file_index.setter
    def selected_file_index(self, value):
        if self._current_file.content == []:
            self._selected_file_index = None
        elif value < 0:
            self._selected_file_index = 0
        elif value > len(self._current_file.content)-1:
            self._selected_file_index = len(self._current_file.content)-1
        else:
            self._selected_file_index = value
