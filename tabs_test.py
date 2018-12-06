#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from tabs import tabs

tabs = tabs(os.path.dirname(os.path.abspath(__file__)))

print(tabs.selected_tab().path)
