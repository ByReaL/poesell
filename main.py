#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import sqlite3

from libs.mystash import MyStash
from libs.poetrade import Items, Currency
from libs.whispers import Whispers

#from xlibs.game import Game

mdb = sqlite3.connect(':memory:', check_same_thread=False)
mdb.row_factory = sqlite3.Row

#game = Game(mdb)
#game.get_mouse_position()
#game.get_win_size()
#game.get_item()

#exit()

whispers = Whispers(mdb)  #always initialize first
mystash = MyStash(mdb)

whispers.monitor(True)
mystash.display_stashes()
mystash.display_items(8)

while True:
    key_in = input('# ')
    print('>%s<' % key_in)
    if key_in is 'exit':
        whispers.monitor(False)
        break
    elif key_in is '':
        mystash.display_stashes()
    elif 'vendor' in key_in:
        words = key_in.split(' ')
        if len(words) == 2:
            stash_index = words[1]
            mystash.vendor(stash_index)
        else:
            mystash.display_stashes()
            print('must provide the stash index')
    elif 'stash' in key_in:
        words = key_in.split(' ')
        if len(words) == 2:
            stash_index = words[1]
            mystash.display_items(stash_index)
        else:
            mystash.display_stashes()
            print('must provide the stash index')
        mystash.display_stashes()
    else:
        pass
