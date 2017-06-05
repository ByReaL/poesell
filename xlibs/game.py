#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import win32api
import win32con
import win32gui
import pywintypes
import win32clipboard
import ctypes
import time
import os
import sys

# regsvr32.exe c:\Python35\AutoHotkey.dll


class Game:

    def __init__(self, mdb):
        self.mdb = mdb
        self.cur = self.mdb.cursor()
        self.ahk = ctypes.cdll.AutoHotkey
        self.ahk.ahktextdll("", "", "")  # start script in persistent mode (wait for action)
        while not self.ahk.ahkReady():
            time.sleep(0.01)

    def get_cords(self):
        x, y = win32api.GetCursorPos()
        print(x, y)

    def mousePos(x, y):
        win32api.SetCursorPos(x, y)

    def get_win_size(self):
        hwnd = win32gui.GetDesktopWindow()
        l, t, r, b = win32gui.GetWindowRect(hwnd)
        print(l, t, r, b)

    def get_item(self):
        win32clipboard.OpenClipboard()
        try:
            got = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            print(got)
        finally:
            win32clipboard.CloseClipboard()
        #win32gui.

    def focus(self):
        code = '''
IfWinExist, Path of Exile
    WinActivate, Path of Exile
else
    MsgBox Path of Exile not found
        '''
        self.ahk.ahkExec(code)

    def get_window_size(self):
        self.focus()
        code = '''
WinGetPos, X, Y, Width, Height, A
'''

    def open_stash(self):
        pass

    def go_to_stash_tab(self, stash_ind):
        pass

    def stash_coordinates_to_pizels(self, stash_x, stash_y):
        pixel_x = 0
        pixel_y = 0
        return pixel_x, pixel_y

    def control_click(self, pixel_x, pixel_y):
        pass

    def move_from_stats_to_inventory(self, stash_ind, stash_x, stash_y):
        self.focus()
        self.open_stash()
        self.go_to_stash_tab(stash_ind)
        pixel_x, pixel_y = self.stash_coordinates_to_pizels(stash_x, stash_y)
        self.control_click(pixel_x, pixel_y)




# ahk.ahkdll(pyclient, "", fx)
# ahk.ahkassign(create_string_buffer("fx"), fx)
# ahk.addScript(script)
# ahk.ahkFunction(create_string_buffer("fx2"), create_string_buffer("Untitled"))