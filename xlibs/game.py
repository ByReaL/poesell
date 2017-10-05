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

    def get_mouse_position(self):
        x, y = win32api.GetCursorPos()
        print(x, y)

    def set_mouse_position(self, x, y):
        win32api.SetCursorPos((x, y))

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
WinGetPos, XZZZ, Y, W, H, Path of Exile
'''
        self.ahk.ahkExec(code)
        self.poe_win_x = self.get_ahk_var('XZZZ')
        print('c')
        self.poe_win_y = self.get_ahk_var('Y')
        self.poe_win_w = self.get_ahk_var('W')
        self.poe_win_h = self.get_ahk_var('H')
        print('%d - %d - %d -%d' % (self.poe_win_x, self.poe_win_y, self.poe_win_w, self.poe_win_h))

    def find_stash(self):
        code = r'''
ImageSearch, FoundX, FoundY, 0,0, 800, 800, C:\GitHub\poesell\xlibs\img\stash.bmp
'''
        self.ahk.ahkExec(code)
        x = self.get_ahk_var('FoundX')
        y = self.get_ahk_var('FoundY')
        return x, y

    def open_stash(self):
        x, y = self.find_stash()
        code = '''
MouseClick, left, %d, %d
''' % (x, y)
        self.ahk.ahkExec(code)
        
    def go_to_stash_tab(self, stash_ind):
        pass

    def stash_coordinates_to_pixels(self, stash_x, stash_y):
        base_x = 0
        base_y = 0
        pixel_x = base_x + (10 * stash_x)
        pixel_y = base_y + (10 * stash_y)
        return pixel_x, pixel_y

    def _evaluate(self, obj):
        casted = ctypes.cast(obj, ctypes.c_char_p)
        print('b2')
        print(casted)
        value = casted.value
        print('b3')
        return eval(value.decode())

    def set_ahk_var(self, variable, value):
        return not self.ahk.ahkassign(variable.encode(), repr(value).encode())

    def get_ahk_var(self, variable, pointer=False):
        p = self.ahk.ahkgetvar(variable.encode('ascii'), ctypes.c_uint(pointer))
        print(p)
        return self._evaluate(p)

    def control_click(self, pixel_x, pixel_y):
        code = '''
Send, {Control down}
MouseClick, left, %d, %d
Send, {Control up}
''' % (pixel_x, pixel_y)
        self.ahk.ahkExec(code)

    def move_from_stats_to_inventory(self, stash_x, stash_y):
        pixel_x, pixel_y = self.stash_coordinates_to_pixels(stash_x, stash_y)
        self.control_click(pixel_x, pixel_y)




# ahk.ahkdll(pyclient, "", fx)
# ahk.ahkassign(create_string_buffer("fx"), fx)
# ahk.addScript(script)
# ahk.ahkFunction(create_string_buffer("fx2"), create_string_buffer("Untitled"))