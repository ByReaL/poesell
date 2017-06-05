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


# ahk.ahkdll(pyclient, "", fx)
# ahk.ahkassign(create_string_buffer("fx"), fx)
# ahk.addScript(script)
# ahk.ahkFunction(create_string_buffer("fx2"), create_string_buffer("Untitled"))