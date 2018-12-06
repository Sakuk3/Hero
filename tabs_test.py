#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from tabs import tabs

tabs = tabs(os.path.dirname(os.path.abspath(__file__)))

print(tabs.get_selected_tab().index)
tabs.switch_tab(2)
print(tabs.get_selected_tab().index)
print('')
for tab in tabs.tab_list:
    print(tab.index)
    print(tab.selected)
