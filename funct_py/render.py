from dataclasses import asdict
import json

def Render(model,window):
    window.clear()
    if model.mode == 0:
        _render_debug(model,window)
    else:
        _render_view(model,window)

def _render_view(model,window):
    rows, cols = window.getmaxyx()
    tablist = "".join([str(tab.index) for tab in model.tabs])

    window.addstr(
            0,
            0,
            "{}@{} {}".format(
                model.username,
                model.hostname,
                model.tabs[model.selected_tab].selected_file.path))
    
    window.addstr(
            0,
            cols-len(tablist),
            tablist)

def _render_debug(model,window):
    rows, cols = window.getmaxyx()
    window.clear()
    pjson = json.dumps(asdict(model), indent=4).split("\n")
    for index,line in enumerate(pjson[:rows]):
        window.addstr(index,0,line[:cols])

def _size_prettyfier(size: int):
    for unit in ['','K','M','G','T','P']:
        if abs(size) < 1024.0:
            return "{size}{unit}b".format(size=round(size,1), unit=unit,)
        size /= 1024.0
    return "NaN"
