from dataclasses import dataclass
from typing import List
import os

@dataclass(frozen=True)
class File:
    path:         str
    is_dir:       bool
    content:      List[str] # is_dir list of Files
    # else readlines

    content_size: int # is_dir    number of files
    # else      size in byte

    @property
    def name(self) -> str:
        if self.path:
            return os.path.basename(self.path)
        else:
            return None

    @property
    def extension(self) -> str:
        if self.name:
            exte = os.path.splitext(self.full_name)[1]
            if exte:
                return exte
            else:
                None
        else:
            return None


@dataclass(frozen=True)
class Tab:
    index:         int
    current_file:  File
    selected_file: File

@dataclass(frozen=True)
class Model:
    tabs:               List[Tab]
    username:           str
    hostname:           str
    selected_tab:       int = 0
    clipbord:           str = None
    mode:               int = 1 # 0 = debug
                                # 1 = browse
    debug_offset:       int = 0
    prev_event:         str = ""
    code_hilighting:    bool = True
    exit:               bool = False
    debug_model_length: int = 0
    debug_model_text:   List[str] = None