#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import requests
import unicodedata

class Items:

    def __init__(self, mdb):
        self.poetrade_url = 'http://poe.trade'
        self.session = self._initialize_session()
        self.mdb = mdb
        self.cur = self.mdb.cursor()
        #self._init_poetrade_db()


    def _initialize_session(self):
        s = requests.session()
        r = s.get(self.poetrade_url)
        query_data = dict(seller='Jilava')
        s.post(self.login_url, data=query_data)
        return s

    def _init_poetrade_db(self):
        self.cur.execute('''CREATE TABLE poetrade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age TEXT,
            price TEXT)''')
        self._load_stash_in_db()

    poe_trade_link = r'http://poe.trade/search/ihotanoanonoka'
    poe_trade_link = r'http://poe.trade/search/orenutonadumek'  # 1 regal
    poe_trade_link = r'http://poe.trade/search/auogohawomatuk'  # 1 vaal

    def load_poe_trade_data(self, link):
        response = urlopen(link)
        html = response.read().splitlines()
        for line in html:
            line = unicodedata.normalize('NFKD', line.decode('utf-8')).encode('ascii', 'replace').decode('ascii')
            # print(line)
            items = tradeextractor.search(line)
            if items is not None:
                try:
                    item = items.group(1)
                    age = items.group(2)
                    offers = self.cur.execute('SELECT COUNT(*) FROM (SELECT * FROM poe WHERE item=? GROUP BY player)',
                                         (item,)).fetchone()[0]

                    items_for_sale.append(PoeTi(item, age, offers))
                except Exception as e:
                    print(line)
                    print(e)


class Currency:

    CURRENCIES = dict({
        1: 'Orb of Alteration',
        2: 'Orb of Fusing',
        3: 'Orb of Alchemy',
        4: 'Chaos Orb',
        5: "Gemcutter's Prism",
        6: 'Exalted Orb',
        7: 'Chromatic Orb',
        8: "Jeweller's Orb",
        9: 'Orb of Chance',
        10: "Cartographer's Chisel",
        11: 'Orb of Scouring',
        12: 'Blessed Orb',
        13: 'Orb of Regret',
        14: 'Regal Orb',
        15: 'Divine Orb',
        16: 'Vaal Orb',
        17: 'Scroll of Wisdom',
        18: 'Portal Scroll',
        19: "Armourer's Scrap",
        20: "Blacksmith's Whetstone",
        21: "Glassblower's Bauble",
        22: 'Orb of Transmutation',
        23: 'Orb of Augmentation',
        24: 'Mirror of Kalandra',
        25: 'Eternal Orb',
        26: 'Perandus Coin',
        27: 'Sacrifice at Dusk',
        28: 'Sacrifice at Midnight',
        29: 'Sacrifice at Dawn',
        30: 'Sacrifice at Noon',
        31: 'Mortal Grief',
        32: 'Mortal Rage',
        33: 'Mortal Hope',
        34: 'Mortal Ignorance',
        35: 'Silver Coin',
        36: "Eber's Key",
        37: "Yriel's Key",
        38: "Inya's Key",
        39: "Volkuur's Key",
        40: "Offering to the Goddess",
    })

    def __init__(self, mdb):
        self.poetrade_url = 'http://poe.trade'
        self.session = self._initialize_session()
        self.mdb = mdb
        self.cur = self.mdb.cursor()
        #self._init_poetrade_db()