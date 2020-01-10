import subprocess
def highlight(file_path):
    command = ["highlight", file_path,"--out-format=truecolor"]
    return subprocess.check_output(command).decode("utf-8")
