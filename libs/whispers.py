#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import io
import os
import re
import sqlite3
import unicodedata
import time

from threading import Thread
from tabulate import tabulate

from settings import POE_LOG_FILE, POE_LEAGUE

whisper_extractor = re.compile('''^([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}).*@From (.*): Hi, I would like to buy your (.*) listed for ([0-9]+) (.*) in %s .*''' % (POE_LEAGUE,))
#2017/05/17 09:43:48 242550390 951 [INFO Client 4196] @From Harvesting_Season: Hi, I would like to buy your Sacrificial Harvest Viridian Jewel listed for 1 fusing in Legacy (stash tab "~b/o 1 fuse"; position: left 1, top 4)

_monitor_state = False

class Whispers:

    def __init__(self, mdb):
        self. row_count = -1
        self.lines_loaded = 0
        self.mdb = mdb
        self.cur = self.mdb.cursor()
        self._init_db()
        self.file_time = os.stat(POE_LOG_FILE).st_size

    def get_count(self):
        self.row_count = self.cur.execute('SELECT COUNT(*) FROM whispers').fetchone()
        return self.row_count

    def _init_db(self):
        self.cur.execute('''CREATE TABLE whispers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Player TEXT,
            Item TEXT,
            Amount INTEGER,
            Currency TEXT)''')
        self._load_log_file_in_db()

    def _load_log_file_in_db(self, start_line=0):
        with io.open(POE_LOG_FILE, 'rt+', encoding='utf-8') as fh:
            lines = fh.readlines()
        for line in lines[start_line:]:
            self.lines_loaded += 1
            if r'Hi, I would like to buy your' in line:
                line = unicodedata.normalize('NFKD', line).encode('ascii', 'replace').decode('ascii')  # hack to get rid of non utf-8 chars
                print(line)
                self._insert_line_in_database(line)
        self.mdb.commit()

    def _insert_line_in_database(self, line):
        items = whisper_extractor.search(line)
        if items is not None:
            try:
                date = items.group(1)
                player = items.group(2)
                item = items.group(3)
                amount = items.group(4)
                currency = items.group(5)
            except Exception as e:
                print(line)
                print(e)
            # date = items.group(5)
            # date = items.group(6)
            # date = items.group(7)
            # date = items.group(8)
            # date = items.group(9)

            self.cur.execute('''
                INSERT INTO whispers (Date, Player, Item, Amount, Currency)
                VALUES (?,?,?,?,?)''', (date, player, item, amount, currency))
        else:
            print('ERROR: ' + line)

    def _get_last_row_id(self):
        return self.cur.execute('SELECT COUNT(*) FROM whispers').fetchone()[0]

    def _get_last_row(self):
        return self.cur.execute('SELECT * FROM whispers ORDER BY id DESC LIMIT 1').fetchone()

    def _monitor_trade_requests(self):
        global _monitor_state
        last_row_id = self._get_last_row_id()
        while _monitor_state:
            time.sleep(1)
            new_file_time = os.stat(POE_LOG_FILE).st_size
            # print(new_file_time)
            if self.file_time != new_file_time:
                self.file_time = new_file_time
                self._load_log_file_in_db(self.lines_loaded)
                self.mdb.commit()
                new_row_id = self._get_last_row_id()
                if new_row_id != last_row_id:
                    last_row_id = new_row_id
                    id, date, player, item, amount, currency = self._get_last_row()
                    self.print_history_on_item(item)

    def print_history_on_item(self, item):
        history = self.cur.execute('SELECT * FROM (SELECT * FROM whispers WHERE item=? ORDER BY id DESC LIMIT 20) ORDER BY id ASC', (item,)).fetchall()
        print(tabulate(history, headers=history[0].keys(), tablefmt='psql'))

    def get_unique_count(self, item):
        return  self.cur.execute('SELECT COUNT(*) FROM (SELECT * FROM whispers WHERE item=? GROUP BY player)', (item,)).fetchone()[0]

    def monitor(self, state):
        global _monitor_state
        if state:
            _monitor_state = True
            Thread(target=self._monitor_trade_requests, args=()).start()
        else:
            _monitor_state = False

