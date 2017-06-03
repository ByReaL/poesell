#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import sqlite3

from libs.mystash import MyStash
from libs.poetrade import PoeTrade
from libs.whispers import Whispers

mdb = sqlite3.connect(':memory:', check_same_thread=False)
mdb.row_factory = sqlite3.Row

whispers = Whispers(mdb)
whispers.monitor(True)
mystash = MyStash(mdb)

mystash.display_stashes()
mystash.display_items(17)

while True:
    key_in = input('# ')
    print('>%s<' % key_in)
    if key_in is 'exit':
        whispers.monitor(False)
        break
    elif key_in is '':
        mystash.display_stashes()
    elif key_in is 'vendor':
        pass
    else:
        pass
