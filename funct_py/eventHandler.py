from dataclasses import replace
import os
import curses

import models
from modelHandler import *

def _up(model: models.Model,event: str):
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

def _down(model: models.Model,event: str):
    return model

def _quit(model: models.Model,event: str):
    return replace(model,exit=True)

def _debug(model: models.Model,event: str):
    if model.mode == 0:
        return replace(model,mode=1)
    else:
        return replace(model,mode=0)

def _deafult(model: models.Model,event: str):
    return model

events = {
    "w":_up,
    "s":_down,
    "q":_quit,
    "d":_debug,
}

def _update_model(model: models.Model):
    return model

def EventHandler(model: models.Model,event: str):
    model = _update_model(model)
    return events.get(event, _deafult)(model,event)
