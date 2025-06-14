import ctypes
from ctypes.wintypes import BOOL, HWND, HANDLE, HGLOBAL, UINT, LPVOID, INT, LPWSTR
from ctypes import c_size_t as SIZE_T
from typing import List, Tuple, Optional
import os

OpenClipboard = ctypes.windll.user32.OpenClipboard
OpenClipboard.argtypes = HWND,
OpenClipboard.restype = BOOL
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
EmptyClipboard.restype = BOOL
GetClipboardData = ctypes.windll.user32.GetClipboardData
GetClipboardData.argtypes = UINT,
GetClipboardData.restype = HANDLE
SetClipboardData = ctypes.windll.user32.SetClipboardData
SetClipboardData.argtypes = UINT, HANDLE
SetClipboardData.restype = HANDLE
CloseClipboard = ctypes.windll.user32.CloseClipboard
CloseClipboard.restype = BOOL
CountClipboardFormats = ctypes.windll.user32.CountClipboardFormats
CountClipboardFormats.restype = INT
EnumClipboardFormats = ctypes.windll.user32.EnumClipboardFormats
EnumClipboardFormats.argtypes = UINT,
EnumClipboardFormats.restype = UINT
GetClipboardFormatName = ctypes.windll.user32.GetClipboardFormatNameW
GetClipboardFormatName.argtypes = UINT, LPWSTR, INT
GetClipboardFormatName.restype = INT

CF_UNICODETEXT = 13

GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalAlloc.argtypes = UINT, SIZE_T
GlobalAlloc.restype = HGLOBAL
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalLock.argtypes = HGLOBAL,
GlobalLock.restype = LPVOID
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
GlobalUnlock.argtypes = HGLOBAL,
GlobalSize = ctypes.windll.kernel32.GlobalSize
GlobalSize.argtypes = HGLOBAL,
GlobalSize.restype = SIZE_T

GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040

unicode_type = type(u'')


def list_clipboard_format() -> List[Tuple[int, str]]:
    """Checks all the available clipboard data formats"""
    buffer = ctypes.create_unicode_buffer(80)
    formats = []
    format_id = EnumClipboardFormats(0)
    while format_id != 0:
        if GetClipboardFormatName(format_id, buffer, 80) > 0:
            formats.append((format_id, buffer.value))
        format_id = EnumClipboardFormats(format_id)
    return formats


def is_windows():
    return os.name == 'nt'


def paste_windows() -> Tuple[str, Optional[str]]:
    """
    Tries to get data in RTF format. If not available, returns normal unicode
    :return: tuple (data_format, string)
    """
    text = None
    OpenClipboard(None)
    formats = list_clipboard_format()
    fmt = next(filter(lambda x: x[1] == "Rich Text Format", formats), (CF_UNICODETEXT, "Unicode"))
    handle = GetClipboardData(fmt[0])
    pcontents = GlobalLock(handle)
    size = GlobalSize(handle)
    if pcontents and size:
        raw_data = ctypes.create_string_buffer(size)
        ctypes.memmove(raw_data, pcontents, size)
        text = raw_data.raw.decode('utf-8').rstrip(u'\0')
    GlobalUnlock(handle)
    CloseClipboard()
    return fmt[1], text
