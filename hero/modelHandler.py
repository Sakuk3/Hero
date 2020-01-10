from models import Model, Tab, File
import os


def file_from_path(path):
    is_dir = os.path.isdir(path)

    if is_dir:
        content = os.listdir(path)
        content_size = len(content)
    else:
        with open(path,"r") as f:
            content = [f.readline().rstrip()]
        content_size = os.path.getsize(path)

    return File(
        path = path,
        is_dir = is_dir,
        content = content,
        content_size = content_size
    )

def init_model(path: str,username: str,hostname: str):
    current_file = file_from_path(path)

    if current_file.is_dir and current_file.content:
        selected_file = file_from_path(os.path.join(path,current_file.content[0]))
    else:
        selected_file = None

    return Model(
        tabs = [Tab(
            index = 0,
            current_file =  current_file,
            selected_file = selected_file,

        )],
        username = username,
        hostname = hostname
    )
