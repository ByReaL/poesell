#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import json
import sqlite3
import re
import requests
import unicodedata
import time
import _thread

from settings import (POE_LOGIN_EMAIL, POE_LOGIN_PASSWORD, POE_LEAGUE)

hash_extractor = re.compile('''\<input type="hidden" name="hash" value="([a-zA-Z0-9]+)" id="hash"\>''')
#<input type="hidden" name="hash" value="ed99f40eec40b691ccf69badb36b5e74" id="hash">

class MyStash:

    def __init__(self):
        self.login_url = 'https://www.pathofexile.com/login'
        self.account_name_url = 'https://www.pathofexile.com/character-window/get-account-name'
        self.session = self._initialize_session()
        self.account_name = self._get_account_name()
        self.stash_url = 'https://www.pathofexile.com/character-window/get-stash-items?league=%s&accountName=%s&tabs=1' % (POE_LEAGUE, self.account_name)
        self.mdb = sqlite3.connect(':memory:', check_same_thread=False)
        self.cur = self.mdb.cursor()
        self._init_stash__db()
        self._init_items__db()
        self.tab_count = 4

    def _initialize_session(self):
        s = requests.session()
        r = s.get(self.login_url)
        hash_value = hash_extractor.search(r.content.decode('utf-8')).group(1)
        login_data = dict(login_email=POE_LOGIN_EMAIL, login_password=POE_LOGIN_PASSWORD, hash=hash_value)
        s.post(self.login_url, data=login_data)
        return s

    def _get_account_name(self):
        r = self.session.get(self.account_name_url)
        # print(r.content)
        data = json.loads(r.content.decode('utf-8'))
        account_name = data['accountName']
        return account_name

    def get_count(self):
        self.row_count = self.cur.execute('SELECT COUNT(*) FROM poe').fetchone()
        return self.row_count

    def _init_stash__db(self):
        self.cur.execute('''CREATE TABLE stash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            index TEXT,
            type TEXT,
            hidden INTEGER)''')
        self._load_stash_in_db()

    def _load_stash_in_db(self):
        stash_url = self.stash_url + r'&tabIndex=0'
        r = self.session.get(stash_url)
        data = json.loads(r.content.decode('utf-8'))
        self.tab_count = int(data['numTabs'])
        poe_tabs = data['tabs']
        for tab in poe_tabs:
            #{"n":"1","i":0,,"type":"NormalStash","hidden":false,},
            self.cur.execute('''
                            INSERT INTO stash      (name,    index,        type,        hidden)
                            VALUES (?,?,?,?)''', (tab['n'], tab['i'], tab['type'], tab['hidden'],))
        self.mdb.commit()

    def _init_items_db(self):
        self.cur.execute('''CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            index TEXT,
            type TEXT,
            hidden INTEGER)''')
        self._load_items_in_db()

    def _load_items_in_db(self):
        for tab_index in range(0,self.tab_count):
            stash_url = self.stash_url + r'&tabIndex=%d' % tab_index
            r = self.session.get(stash_url)
            data = json.loads(r.content.decode('utf-8'))
            is_selected = data['tabs'][tab_index]['selected']
            if is_selected:
                items = data['items']
                for item in items:
                    self.cur.execute('''
                                    INSERT INTO items        (name,    index,        type,        hidden)
                                    VALUES (?,?,?,?)''', (tab['n'], tab['i'], tab['type'], tab['hidden'],))
                self.mdb.commit()
            else:
                print('could not load the items from the tab %d' % tab_index)

