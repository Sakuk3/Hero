import subprocess
def highlight(file_path):
    command = ["highlight", "hero.py","--out-format=truecolor"]
    s=subprocess.check_output(command).decode("utf-8")
    print(s)