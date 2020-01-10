import subprocess
import sys

"""
    ansi:      Terminal 16 color escape codes
    xterm256:  Terminal 256 color escape codes
    truecolor: Terminal 16m color escape codes
"""
output_format = "truecolor"

def highlight(input: str,syntax_style: str):
    p = subprocess.Popen(
        [
            "highlight",
            "--syntax={}".format(syntax_style),
            "--out-format={}".format(output_format)
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    output = p.communicate(input=input.encode())[0].decode()
    return output

def highlight_list(input: list,syntax_style: str):
    return highlight("\n".join(input),syntax_style).split("\n")