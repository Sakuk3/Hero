from dataclasses import replace, asdict
import os
import curses
import json

import models
from modelHandler import *
from highlight import highlight


def _browse_up(model: models.Model,event: str):
    if model.tabs[model.selected_tab].current_file.is_dir:
        return replace(model,
            tabs = [
                tab
                if tab.index != model.selected_tab else
                replace(
                    tab,
                    selected_file = file_from_path("/home/sakuk/Documents/Hero/funct_py")
                )
                for tab in model.tabs
            ]
        )

    else:
        return model

def _browse_down(model: models.Model,event: str):
    return model

def _debug_up(model: models.Model,event: str):
    return replace(model,debug_offset=max(model.debug_offset-1, 0))

def _debug_down(model: models.Model,event: str):
    return replace(model,debug_offset=min(
        model.debug_offset+1, 
        model.debug_model_length-1
    ))

def _quit(model: models.Model,event: str):
    return replace(model,exit=True)

def _debug(model: models.Model,event: str):
    model= replace(model,mode=0)

    model_dict = asdict(model)
    model_dict.pop("debug_model_length")
    model_dict.pop("debug_model_text")
    model_json = json.dumps(model_dict, indent=2)

    if model.code_hilighting:
        model= replace(model,debug_model_text=highlight(model_json,"json").split("\n"))
    else:
        model= replace(model,debug_model_text=model_json.split("\n"))

    model= replace(model,debug_model_length=len(model.debug_model_text))
    return model

def _browse(model: models.Model,event: str):
    return replace(model,mode=1)

def _default(model: models.Model,event: str):
    return model

events_browse = {
    "q":_quit,
    "d":_debug,
    "w":_browse_up,
    "s":_browse_down,
    "[A":_browse_up,
    "[B":_browse_down,
}

events_debug = {
    "q":_quit,
    "d":_browse,
    "w":_debug_up,
    "s":_debug_down,
    "[A":_debug_up,
    "[B":_debug_down,
}

modes = {
    "0":events_debug,
    "1":events_browse,
}

def _mode_handeler(model: models.Model,event: str):
    replace(model,mode=1)

def _update_model(model: models.Model,event: str):
    return replace(model,prev_event=event)

def EventHandler(model: models.Model,event: str):
    model = modes.get(str(model.mode),_mode_handeler).get(event, _default)(model,event)
    return _update_model(model,event)