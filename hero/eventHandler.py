from dataclasses import replace, asdict
import os
import curses
import json

import blesses
import models
from modelHandler import *
from highlight import highlight


def _browse_up(model: models.Model, event: str):
    if model.tabs[model.selected_tab].current_file.is_dir:
        selected_file_index = max(
            model.tabs[model.selected_tab].current_file.content.index(
                os.path.basename(
                    model.tabs[model.selected_tab].selected_file.path)
            )-1,
            0
        )

        return replace(model,
                       tabs=[
                           tab
                           if tab.index != model.selected_tab else
                           replace(
                               tab,
                               selected_file=file_from_path(
                                   os.path.join(
                                       model.tabs[model.selected_tab].current_file.path,
                                       model.tabs[model.selected_tab].current_file.content[selected_file_index]
                                   )
                               )
                           )
                           for tab in model.tabs
                       ]
                       )
    else:
        return model


def _browse_down(model: models.Model, event: str):
    if model.tabs[model.selected_tab].current_file.is_dir:
        selected_file_index = min(
            model.tabs[model.selected_tab].current_file.content.index(
                os.path.basename(
                    model.tabs[model.selected_tab].selected_file.path)
            )+1,
            len(model.tabs[model.selected_tab].current_file.content)-1
        )

        return replace(model,
                       tabs=[
                           tab
                           if tab.index != model.selected_tab else
                           replace(
                               tab,
                               selected_file=file_from_path(
                                   os.path.join(
                                       model.tabs[model.selected_tab].current_file.path,
                                       model.tabs[model.selected_tab].current_file.content[selected_file_index]
                                   )
                               )
                           )
                           for tab in model.tabs
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


def _quit(model: models.Model, event: str):
    return replace(model, exit=True)


def _debug(model: models.Model, event: str):
    model = replace(model, mode=0)

    model_dict = asdict(model)
    model_dict.pop("debug_model_length")
    model_dict.pop("debug_model_text")
    model_dict['tabs'][model_dict['selected_tab']]['selected_file']['content'] = [
        blesses.strip_esc(line) for
        line in model_dict['tabs'][model_dict['selected_tab']
                                   ]['selected_file']['content']
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
    elif [True for tab in model.tabs if tab.index == int(event)]:
        return replace(model, selected_tab=event)

    # If tab dosn't exists
    else:
        return replace(
            replace(model,
                    tabs=model.tabs + [replace(
                        model.tabs[model.selected_tab],
                        index=event
                    )]
                    ),
            selected_tab=int(event))


def _events_browse(model: models.Model, event: str):
    events = {
        "q": _quit,
        "d": _debug,
        "w": _browse_up,
        "s": _browse_down,
        "[A": _browse_up,
        "[B": _browse_down,
    }

    if event.isdigit():
        return _switch_tabs(model, event)

    return events.get(event, _default)(model, event)


def _events_debug(model: models.Model, event: str):
    events = {
        "q": _quit,
        "d": _browse,
        "w": _debug_up,
        "s": _debug_down,
        "[A": _debug_up,
        "[B": _debug_down,
    }

    if event.isdigit():
        return _switch_tabs(model, event)

    return events.get(event, _default)(model, event)


modes = {
    "0": _events_debug,
    "1": _events_browse,
}


def _mode_handeler(model: models.Model, event: str):
    replace(model, mode=1)


def EventHandler(model: models.Model, event: str):
    return modes.get(str(model.mode), _mode_handeler)(model, event)
