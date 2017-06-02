#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

from libs.mystash import MyStash
from libs.poetrade import PoeTrade
from libs.whispers import Whispers


#whispers = Whispers()
#whispers.monitor(True)
mystash = MyStash()

mystash.display()

while True:
    key_in = input('# ')
    print('>%s<' % key_in)
    if key_in is 'exit':
        #whispers.monitor(False)
        break
    elif key_in is '':
        pass
    elif key_in is 'vendor':
        pass
    else:
        pass
