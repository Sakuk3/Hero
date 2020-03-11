import os
from itertools import islice

from models import Model, Tab, File
from highlight import highlight_list


def file_from_path(path):
    is_dir = os.path.isdir(path)

    if is_dir:
        content = os.listdir(path)
        content_size = len(content)
    else:
        try:
            with open(path,"r") as f:
                content = [line.rstrip() for line in islice(f, 100)]
            content = highlight_list(content,os.path.splitext(path)[1][1:])
            content_size = os.path.getsize(path)
        except (IOError,PermissionError,UnicodeDecodeError):
            content = []
            content_size = 0

    return File(
        path = path,
        is_dir = is_dir,
        content = content,
        content_size = content_size
    )

def create_tab(path: str,selected_file: File = None):
    current_file = file_from_path(path)

    if not selected_file:
        if current_file.is_dir and current_file.content:
            selected_file = file_from_path(os.path.join(path,current_file.content[0]))
        else:
            selected_file = None
    
    return Tab(
        current_file =  current_file,
        selected_file = selected_file,
    )

def init_model(path: str,username: str,hostname: str):
    return Model(
        tabs = [create_tab(path)] + [None]*9,
        username = username,
        hostname = hostname
    )
