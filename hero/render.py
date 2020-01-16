from dataclasses import asdict
import json
import blesses
import models
import os


def Render(model: models.Model):
    blesses.clear_terminal()
    rows, cols = blesses.get_max_row_col()

    if model.mode == 0:
        _render_debug(model, rows, cols)
    else:
        _render_view(model, rows, cols)

    blesses.draw()


def _render_view(model: models.Model, rows: int, cols: int):
    rows, cols = blesses.get_max_row_col()
    _render_current_directory(model, rows, cols)
    _render_preview(model, rows, cols)
    _render_statusbar(model, cols)


def _render_statusbar(model: models.Model, cols: int):
    tab_list = "".join([blesses.inverse(tab.index) if tab.index ==
                        model.selected_tab else str(tab.index) for tab in model.tabs])

    blesses.add_str(
        0,
        0,
        "{}@{} {}".format(
            model.username,
            model.hostname,
            model.tabs[model.selected_tab].selected_file.path))

    blesses.add_str(
        0,
        cols-len(blesses.strip_esc(tab_list)),
        str(tab_list))


def _render_current_directory(model: models.Model, rows: int, cols: int):
    width = 30
    blesses.display_list(
        rows-2,
        width,
        1,
        0,
        model.tabs[model.selected_tab].current_file.content,
        selected_item=os.path.basename(
            model.tabs[model.selected_tab].selected_file.path)
    )


def _render_preview(model: models.Model, rows: int, cols: int):
    width = cols-30
    blesses.display_list(
        rows-2,
        width,
        1,
        30,
        model.tabs[model.selected_tab].selected_file.content,
        line_numbers=not model.tabs[model.selected_tab].selected_file.is_dir
    )


def _render_debug(model: models.Model, rows: int, cols: int):
    rows, cols = blesses.get_max_row_col()
    blesses.clear_terminal()
    blesses.display_list(
        rows,
        cols,
        0,
        0,
        model.debug_model_text,
        list_offsset=model.debug_offset,
        line_numbers=False)


def _size_prettyfier(size: int):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if abs(size) < 1024.0:
            return "{size}{unit}b".format(size=round(size, 1), unit=unit,)
        size /= 1024.0
    return "NaN"
