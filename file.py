import os
from itertools import islice
class File_manager:
    def __init__(self):
        self.files = []

    def get_file(self,path):
        selected_file = [file for file in self.files if file.path == path]
        if selected_file:
            return selected_file[0]
        else:
            new_file = File(path,self)
            self.files.append(new_file)
            return new_file

class File:
    def __init__(self,path,file_manager):
        self._path = path
        self._file_manager = file_manager

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        if self.is_file:
            return os.path.splitext(self.full_name)[0]
        else:
            return os.path.basename(self._path)

    @property
    def full_name(self):
        return os.path.basename(self._path)

    @property
    def extension(self):
        if self.is_file:
            return os.path.splitext(self.full_name)[1]
        else:
            return ""

    @property
    def is_file(self):
        return os.path.isfile(self._path)

    @property
    def is_dir(self):
        return  os.path.isdir(self._path)

    @property
    def content(self):
        if self.is_dir:
            content = []
            for file_name in os.listdir(self._path):
                content.append(self._file_manager.get_file(os.path.join(self.path,file_name)))
            return content
        else:
            return []

    @property
    def preview(self):
        if self.is_file:
            with open(self._path) as f:
                return list(islice(f, 100))
        else:
            return None

    @property
    def parent_dir(self):
        if os.path.dirname(self.path) == self.path:
            return None
        else:
            return self._file_manager.get_file(os.path.dirname(self.path))

    @property
    def size(self):
        return self._path
