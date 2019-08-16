import os
import errno
import config
from itertools import islice
class File_manager:
    def __init__(self):
        self.files = []

    def get_file(self,path):
        selected_file = [file for file in self.files if file.path == path]
        if selected_file:
            if os.path.exists(path):
                return selected_file[0]
        else:
            if os.path.exists(path):
                new_file = File(path,self)
                self.files.append(new_file)
                return new_file

        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

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
                if file_name.startswith("."):
                    if config.SHOW_HIDDEN:
                        content.append(self._file_manager.get_file(os.path.join(self.path,file_name)))
                else:
                    content.append(self._file_manager.get_file(os.path.join(self.path,file_name)))
            return content
        else:
            return []

    @property
    def preview(self):
        if self.is_file:
            try:
                with open(self._path) as f:
                    return list(islice(f, 100))
            except UnicodeDecodeError:
                pass # Fond non-text data
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
        if self.is_dir:
            if config.SHOW_HIDDEN:
                return str(len([file for file in os.listdir(self._path) if not file.startswith(".")]))
            else:
                return str(len(os.listdir(self._path)))
        else:
            num = os.path.getsize(self._path)
            for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
                if abs(num) < 1024.0:
                    return "%3.1f%s%s" % (num, unit, 'B')
                num /= 1024.0
            return "%.1f%s%s" % (num, 'Yi', 'B')
