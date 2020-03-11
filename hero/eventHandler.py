from dataclasses import replace, asdict
import os
import curses
import json

import blesses
import models
from modelHandler import file_from_path, create_tab
from highlight import highlight


def _browse_up(model: models.Model, event: str):
    if model.tabs[model.selected_tab].current_file.is_dir and model.tabs[model.selected_tab].current_file.content:
        selected_file_index = max(
            # get index of selected file in context list
            model.tabs[model.selected_tab].current_file.content.index(
                os.path.basename(
                    model.tabs[model.selected_tab].selected_file.path)
            )-1,
            0
        )

        return replace(model,
                       tabs=[
                           tab
                           if not tab or idx != model.selected_tab else
                           replace(
                               tab,
                               selected_file=file_from_path(
                                   os.path.join(
                                       model.tabs[model.selected_tab].current_file.path,
                                       model.tabs[model.selected_tab].current_file.content[selected_file_index]
                                   )
                               )
                           )
                           for idx, tab in enumerate(model.tabs)
                       ]
                       )
    else:
        return model


def _browse_down(model: models.Model, event: str):
    if model.tabs[model.selected_tab].current_file.is_dir and model.tabs[model.selected_tab].current_file.content:

        selected_file_index = min(
            # get index of selected file in context list
            model.tabs[model.selected_tab].current_file.content.index(
                os.path.basename(
                    model.tabs[model.selected_tab].selected_file.path)
            )+1,
            len(model.tabs[model.selected_tab].current_file.content)-1
        )

        return replace(model,
                       tabs=[
                           tab
                           if  not tab or idx != model.selected_tab else
                           replace(
                               tab,
                               selected_file=file_from_path(
                                   os.path.join(
                                       model.tabs[model.selected_tab].current_file.path,
                                       model.tabs[model.selected_tab].current_file.content[selected_file_index]
                                   )
                               )
                           )
                           for idx, tab in enumerate(model.tabs)
                       ]
                       )
    else:
        return model


def _browse_parent(model: models.Model, event: str):
    if  not model.tabs[model.selected_tab].current_file.path == "/":
        return replace(model,
                       tabs=[
                           tab
                           if  not tab or idx != model.selected_tab else
                           create_tab(
                               os.path.dirname(tab.current_file.path),
                               file_from_path(model.tabs[model.selected_tab].current_file.path)
                               )
                           for idx, tab in enumerate(model.tabs)
                       ]
                       )
    else:
        return model


def _browse_child(model: models.Model, event: str):
    if model.tabs[model.selected_tab].selected_file and model.tabs[model.selected_tab].selected_file.is_dir:
        return replace(model,
                       tabs=[
                           tab
                           if  not tab or idx != model.selected_tab else
                           create_tab(tab.selected_file.path)
                           for idx, tab in enumerate(model.tabs)
                       ]
                       )
    else:
        return model


def _debug_up(model: models.Model, event: str):
    return replace(model, debug_offset=max(model.debug_offset-1, 0))


def _debug_down(model: models.Model, event: str):
    return replace(model, debug_offset=min(
        model.debug_offset+1,
        model.debug_model_length-1
    ))


def _copy(model: models.Model, event: str):
    if model.tabs[model.selected_tab].selected_file:
        return replace(model, clipbord=model.tabs[model.selected_tab].selected_file.path)
    else:
        return model

def _quit(model: models.Model, event: str):
    return replace(model, exit=True)


def _debug(model: models.Model, event: str):
    model = replace(model, mode=0)

    model_dict = asdict(model)
    model_dict.pop("debug_model_length")
    model_dict.pop("debug_model_text")
    
    # strip Escape sequences from highlighted content for readability 
    for tab in model_dict['tabs']:
        if tab and not tab['selected_file']['is_dir']:
            tab['selected_file']['content'] = [
                blesses.strip_esc(line) for
                line in tab['selected_file']['content']
            ]

    model_json = json.dumps(model_dict, indent=2)

    if model.code_hilighting:
        model = replace(model, debug_model_text=highlight(
            model_json, "json").split("\n"))
    else:
        model = replace(model, debug_model_text=model_json.split("\n"))

    model = replace(
        model, debug_model_text=model.debug_model_text[0:len(model.debug_model_text)-1])

    model = replace(model, debug_model_length=len(model.debug_model_text))
    return model


def _browse(model: models.Model, event: str):
    return replace(model, mode=1)


def _default(model: models.Model, event: str):
    return model


def _switch_tabs(model: models.Model, event: str):
    if model.selected_tab == int(event):
        return model

    # If tab already exists
    elif [True for idx, tab in enumerate(model.tabs) if tab and idx == int(event)]:
        return replace(model, selected_tab=int(event))

    # If tab dosn't exists
    else:
        return replace(
            replace(model,
                        tabs=[
                            tab
                            if idx is not int(event) else
                                model.tabs[model.selected_tab]
                            for idx, tab in enumerate(model.tabs) 
                        ]
                    ),
            selected_tab=int(event))


def _events_browse(model: models.Model, event: str):
    events = {
        "q": _quit,
        "g": _debug,
        "w": _browse_up,
        "[A": _browse_up,
        "s": _browse_down,
        "[B": _browse_down,
        "a":_browse_parent,
        "[D":_browse_parent,
        "d":_browse_child,
        "[C":_browse_child,
        "c":_copy

    }

    if event.isdigit():
        return _switch_tabs(model, event)

    return events.get(event, _default)(model, event)


def _events_debug(model: models.Model, event: str):
    events = {
        "q": _quit,
        "g": _browse,
        "w": _debug_up,
        "s": _debug_down,
        "[A": _debug_up,
        "[B": _debug_down,
    }

    return events.get(event, _default)(model, event)


modes = {
    "0": _events_debug,
    "1": _events_browse,
}


def _mode_handeler(model: models.Model, event: str):
    replace(model, mode=1)


def EventHandler(model: models.Model, event: str):
    return modes.get(str(model.mode), _mode_handeler)(model, event)
