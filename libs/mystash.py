#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import json
import re
import requests
import unicodedata
import time
import _thread

from tabulate import tabulate

from settings import (POE_LOGIN_EMAIL, POE_LOGIN_PASSWORD, POE_LEAGUE)

hash_extractor = re.compile('''\<input type="hidden" name="hash" value="([a-zA-Z0-9]+)" id="hash"\>''')
#<input type="hidden" name="hash" value="ed99f40eec40b691ccf69badb36b5e74" id="hash">


class MyStash:

    def __init__(self, mdb):
        self.login_url = 'https://www.pathofexile.com/login'
        self.account_name_url = 'https://www.pathofexile.com/character-window/get-account-name'
        self.session = self._initialize_session()
        self.account_name = self._get_account_name()
        self.stash_url = 'https://www.pathofexile.com/character-window/get-stash-items?league=%s&accountName=%s&tabs=1' % (POE_LEAGUE, self.account_name)
        self.mdb = mdb
        self.cur = self.mdb.cursor()
        self._init_stash_db()
        self._init_items_db()
        self.stash_count = 4

    def _initialize_session(self):
        s = requests.session()
        r = s.get(self.login_url)
        hash_value = hash_extractor.search(r.content.decode('utf-8')).group(1)
        #print(hash_value)
        login_data = dict(login_email=POE_LOGIN_EMAIL, login_password=POE_LOGIN_PASSWORD, hash=hash_value)
        s.post(self.login_url, data=login_data)
        return s

    def _get_account_name(self):
        r = self.session.get(self.account_name_url)
        data = json.loads(r.content.decode('utf-8'))
        if 'false' in data:
            print('invalid login')
            exit(0)
        account_name = data['accountName']
        print('POE account %s successfully logged in' % (account_name,))
        return account_name

    #def get_count(self):
    #    self.row_count = self.cur.execute('SELECT COUNT(*) FROM poe').fetchone()
    #    return self.row_count

    def _init_stash_db(self):
        self.cur.execute('''CREATE TABLE stash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ind INTEGER,
            type TEXT,
            hidden NUMERIC)''')
        self._load_stash_in_db()

    def _load_stash_in_db(self):
        stash_url = self.stash_url + r'&tabIndex=0'
        r = self.session.get(stash_url)
        data = json.loads(r.content.decode('utf-8'))
        self.stash_count = int(data['numTabs'])
        poe_tabs = data['tabs']
        for tab in poe_tabs:
            #{"n":"1","i":0,,"type":"NormalStash","hidden":false,},
            self.cur.execute('''
                            INSERT INTO stash      (name,      ind,        type,        hidden)
                            VALUES (?,?,?,?)''', (tab['n'], tab['i'], tab['type'], tab['hidden'],))
        self.mdb.commit()

    def _init_items_db(self):
        self.cur.execute('''CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            stash_ind INTEGER,
            w INTEGER,
            h INTEGER,
            x INTEGER,
            y INTEGER,
            price INTEGER,
            currency TEXT,
            type TEXT,
            ilvl INTEGER,
            whispers INTEGER)''')
        self._load_items_in_db()

    def _load_items_in_db(self):
        for stash_ind in range(0,self.stash_count):
            stash_url = self.stash_url + r'&tabIndex=%d' % stash_ind
            r = self.session.get(stash_url)
            data = json.loads(r.content.decode('utf-8'))
            stash_name = data['tabs'][stash_ind]['n']
            is_selected = data['tabs'][stash_ind]['selected']
            if is_selected:
                items = data['items']
                for item in items:
                    # data_examples/item.json
                    name = self.__get_item_name(item['name'], item['typeLine'])
                    # stash_ind from for loop
                    w = item['w']
                    h = item['h']
                    x = item['x']
                    y = item['y']
                    #print(item)
                    if 'note' in item.keys():
                        _note = item['note']
                    else:
                        _note = ''
                    price = self.__get_item_price(_note, stash_name)
                    currency = self.__get_item_currency(_note, stash_name)
                    type = self.__get_item_type(item['frameType'])
                    ilvl = item['ilvl']
                    from main import whispers
                    wcnt = whispers.get_unique_count(name)
                    self.cur.execute('''
                                    INSERT INTO items                  (name, stash_ind, w, h, x, y, price, currency, type, ilvl, whispers)
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (name, stash_ind, w, h, x, y, price, currency, type, ilvl, wcnt,))
                self.mdb.commit()
            else:
                print('could not load the items from the tab %d' % stash_ind)

    def __get_item_name(self, line1, line2):
        item_name = line1.replace('<<set:MS>><<set:M>><<set:S>>', '')
        item_name += ' ' + line2.replace('<<set:MS>><<set:M>><<set:S>>', '')
        return item_name

    def __get_item_price(self, note, stash_name):
        if '~' in note:
            return note.split(' ')[1]
        elif '~' in stash_name:
            return stash_name.split(' ')[1]
        else:
            return 0

    def __get_item_currency(self, note, stash_name):
        if '~' in note:
            return note.split(' ')[2]
        elif '~' in stash_name:
            return stash_name.split(' ')[2]
        else:
            return 'NA'

    def __get_item_type(self, raw_data):
        types = {
            0: 'normal',
            1: 'magic',
            2: 'rare',
            3: 'unique',
            4: 'TBD',
            5: 'TBD',
            6: 'TBD',
            7: 'TBD',
            8: 'TBD',
            8: 'TBD',
            9: 'TBD',
            10: 'TBD',
            11: 'TBD',
            12: 'TBD',
        }
        return types[raw_data]

    def _to_chaos(self, amount, currency):
        chaos_rate = {
            'NA'    : 0,
            'chaos' : 1,
            'vaal'  : 0.9,
            'alt'   : 0.1,
            'regal' : 0.8,
            'chrom' : 0.07,
        }
        return amount * chaos_rate[currency]

    def display_stashes(self):
        details = self.cur.execute('''SELECT * FROM stash''').fetchall()
        print(tabulate(details, headers=details[0].keys(), tablefmt='psql'))

    def display_items(self, stash):
        details = self.cur.execute('''SELECT * FROM items WHERE stash_ind=?''', (stash, )).fetchall()
        print(tabulate(details, headers=details[0].keys(), tablefmt='psql'))