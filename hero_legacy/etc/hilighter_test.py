import subprocess
command = ["highlight", "hero.py","--out-format=truecolor"]
s=subprocess.check_output(command).decode("utf-8")
print(len(s.split("\n")))
#print(s)
