#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import getpass
from dataclasses import replace, asdict
import signal
import json
import sys

import blesses

from models import Model, Tab, File
from render import Render
from eventHandler import EventHandler
from modelHandler import init_model


def main():
    model = init_model(
        os.path.dirname(os.path.abspath(__file__)),
        getpass.getuser(),
        os.uname().nodename
    )

    def resize(signum, frame):
        Render(model)

    # Re-renders Terminal in case of SIGWINCH(resize) event
    signal.signal(signal.SIGWINCH, resize)

    while not model.exit:
        try:
            Render(model)
            try:
                model = EventHandler(model, blesses.get_key())
            except KeyboardInterrupt:
                model = replace(model, exit=1)
        except Exception as e:
            with open("crash.json", "w+") as f:
                f.write(json.dumps(asdict(model),indent=4))

            raise e


if __name__ == '__main__':
    blesses.wrapper(main)
