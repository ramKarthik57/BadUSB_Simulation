"""
Windows Raw Input (WM_INPUT) Hardware Attribution Monitor
Module: src.detection.raw_input_monitor

Enables per-device hardware attribution for keyboard events on Windows
using the Raw Input API (RegisterRawInputDevices, GetRawInputDeviceInfoW).
Extracts device handles, USB Vendor ID (VID), and Product ID (PID).
"""

import ctypes
from ctypes import wintypes
import platform
import re
import threading
import time
from typing import Callable, Dict, List, Optional


# Win32 Constants
RIM_TYPEMOUSE = 0
RIM_TYPEKEYBOARD = 1
RIM_TYPEHID = 2

RIDEV_INPUTSINK = 0x00000100
RIDEV_REMOVE = 0x00000001
RID_HEADER = 0x10000005
RID_INPUT = 0x10000003
RIDI_DEVICENAME = 0x20000007
RIDI_DEVICEINFO = 0x2000000b

WM_INPUT = 0x00FF
HWND_MESSAGE = ctypes.c_void_p(-3)


# 64-bit Clean Win32 Structures
class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", POINT),
    ]


class RAWINPUTDEVICELIST(ctypes.Structure):
    _fields_ = [
        ("hDevice", wintypes.HANDLE),
        ("dwType", wintypes.DWORD),
    ]


class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", wintypes.USHORT),
        ("usUsage", wintypes.USHORT),
        ("dwFlags", wintypes.DWORD),
        ("hwndTarget", wintypes.HWND),
    ]


class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD),
        ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE),
        ("wParam", wintypes.WPARAM),
    ]


WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.c_longlong,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)


class WNDCLASSEXW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HICON),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
        ("hIconSm", wintypes.HICON),
    ]


class RawInputDeviceInfo:
    def __init__(self, handle_val: int, path: str):
        self.handle_val = handle_val
        self.handle_hex = f"0x{handle_val:X}" if handle_val else "0x0"
        self.path = path
        self.vid = "UNKNOWN"
        self.pid = "UNKNOWN"
        self.name = "Generic Keyboard"
        self.is_espressif = False

        self._parse_path()

    def _parse_path(self):
        if not self.path:
            return
        vid_match = re.search(r"VID_([0-9A-Fa-f]{4})", self.path, re.IGNORECASE)
        pid_match = re.search(r"PID_([0-9A-Fa-f]{4})", self.path, re.IGNORECASE)

        if vid_match:
            self.vid = vid_match.group(1).upper()
        if pid_match:
            self.pid = pid_match.group(1).upper()

        if "303A" in self.vid or "303a" in self.path:
            self.is_espressif = True
            self.name = f"ESP32-S3 BadUSB HID (VID:{self.vid} PID:{self.pid})"
        elif "ACPI" in self.path:
            self.name = f"Internal Built-in Keyboard ({self.path.split('#')[1] if '#' in self.path else 'ACPI'})"
        elif vid_match and pid_match:
            self.name = f"External USB Keyboard (VID:{self.vid} PID:{self.pid})"


class RawInputMonitor:
    """
    Background listener for Windows Raw Input events to perform per-device attribution.
    """

    def __init__(self, on_event_callback: Optional[Callable[[str, float], None]] = None):
        self.on_event_callback = on_event_callback
        self.is_windows = platform.system() == "Windows"
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._hwnd = None
        self._cls_name = None
        self._wnd_proc_ref = None

        self.devices: Dict[str, RawInputDeviceInfo] = {}
        self.active_device_id: Optional[str] = None
        self.active_device_info: Optional[RawInputDeviceInfo] = None

        if self.is_windows:
            self._init_win32()
            self.enumerate_devices()

    def _init_win32(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

        self.user32.DefWindowProcW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.DefWindowProcW.restype = ctypes.c_longlong

        self.user32.GetRawInputData.argtypes = [
            ctypes.c_void_p,
            wintypes.UINT,
            ctypes.c_void_p,
            ctypes.POINTER(wintypes.UINT),
            wintypes.UINT,
        ]
        self.user32.GetRawInputData.restype = wintypes.UINT

        self.user32.GetRawInputDeviceList.argtypes = [
            ctypes.POINTER(RAWINPUTDEVICELIST),
            ctypes.POINTER(wintypes.UINT),
            wintypes.UINT,
        ]
        self.user32.GetRawInputDeviceList.restype = wintypes.UINT

        self.user32.GetRawInputDeviceInfoW.argtypes = [
            wintypes.HANDLE,
            wintypes.UINT,
            ctypes.c_void_p,
            ctypes.POINTER(wintypes.UINT),
        ]
        self.user32.GetRawInputDeviceInfoW.restype = wintypes.UINT

        self.user32.RegisterRawInputDevices.argtypes = [
            ctypes.POINTER(RAWINPUTDEVICE),
            wintypes.UINT,
            wintypes.UINT,
        ]
        self.user32.RegisterRawInputDevices.restype = wintypes.BOOL

        self.user32.RegisterClassExW.argtypes = [ctypes.POINTER(WNDCLASSEXW)]
        self.user32.RegisterClassExW.restype = wintypes.ATOM

        self.user32.CreateWindowExW.argtypes = [
            wintypes.DWORD,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.DWORD,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.HWND,
            wintypes.HMENU,
            wintypes.HINSTANCE,
            wintypes.LPVOID,
        ]
        self.user32.CreateWindowExW.restype = wintypes.HWND

        self.user32.DestroyWindow.argtypes = [wintypes.HWND]
        self.user32.DestroyWindow.restype = wintypes.BOOL

        self.user32.GetMessageW.argtypes = [
            ctypes.POINTER(MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self.user32.GetMessageW.restype = wintypes.BOOL

        self.user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
        self.user32.TranslateMessage.restype = wintypes.BOOL

        self.user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
        self.user32.DispatchMessageW.restype = ctypes.c_longlong

        self.user32.PostMessageW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.PostMessageW.restype = wintypes.BOOL

    def enumerate_devices(self) -> Dict[str, RawInputDeviceInfo]:
        """Query system for all registered keyboard devices."""
        if not self.is_windows:
            return {}

        num_devices = wintypes.UINT()
        self.user32.GetRawInputDeviceList(
            None,
            ctypes.byref(num_devices),
            ctypes.sizeof(RAWINPUTDEVICELIST),
        )
        if num_devices.value == 0:
            return {}

        device_list = (RAWINPUTDEVICELIST * num_devices.value)()
        self.user32.GetRawInputDeviceList(
            device_list,
            ctypes.byref(num_devices),
            ctypes.sizeof(RAWINPUTDEVICELIST),
        )

        for dev in device_list:
            if dev.dwType == RIM_TYPEKEYBOARD:
                handle_val = dev.hDevice if isinstance(dev.hDevice, int) else (dev.hDevice.value if hasattr(dev.hDevice, 'value') else 0)
                handle_hex = f"0x{handle_val:X}"

                name_len = wintypes.UINT()
                self.user32.GetRawInputDeviceInfoW(
                    dev.hDevice,
                    RIDI_DEVICENAME,
                    None,
                    ctypes.byref(name_len),
                )
                path = ""
                if name_len.value > 0:
                    name_buf = ctypes.create_unicode_buffer(name_len.value)
                    self.user32.GetRawInputDeviceInfoW(
                        dev.hDevice,
                        RIDI_DEVICENAME,
                        name_buf,
                        ctypes.byref(name_len),
                    )
                    path = name_buf.value

                dev_info = RawInputDeviceInfo(handle_val, path)
                self.devices[handle_hex] = dev_info

        return self.devices

    def start(self) -> bool:
        """Start background message-only window and event pump."""
        if not self.is_windows or self.running:
            return False

        self.running = True
        self._thread = threading.Thread(target=self._run_message_pump, daemon=True)
        self._thread.start()
        return True

    def stop(self) -> None:
        """Stop background message pump."""
        if not self.running:
            return
        self.running = False
        if self._hwnd and self.is_windows:
            try:
                self.user32.PostMessageW(self._hwnd, 0x0012, 0, 0) # WM_QUIT
            except Exception:
                pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.3)
        self._hwnd = None

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_INPUT:
            # Query Raw Input header to determine device handle
            raw_header = RAWINPUTHEADER()
            header_size = wintypes.UINT(ctypes.sizeof(RAWINPUTHEADER))

            res = self.user32.GetRawInputData(
                lparam,
                RID_HEADER,
                ctypes.byref(raw_header),
                ctypes.byref(header_size),
                ctypes.sizeof(RAWINPUTHEADER),
            )
            if res != 0xFFFFFFFF and raw_header.dwType == RIM_TYPEKEYBOARD:
                handle_val = raw_header.hDevice if isinstance(raw_header.hDevice, int) else (raw_header.hDevice.value if hasattr(raw_header.hDevice, 'value') else 0)
                handle_hex = f"0x{handle_val:X}"

                if handle_hex not in self.devices:
                    self.enumerate_devices()

                self.active_device_id = handle_hex
                self.active_device_info = self.devices.get(
                    handle_hex,
                    RawInputDeviceInfo(handle_val, "Unknown"),
                )

                now_ms = time.perf_counter() * 1000.0
                if self.on_event_callback:
                    try:
                        self.on_event_callback(handle_hex, now_ms)
                    except Exception:
                        pass

            return 0

        return self.user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _run_message_pump(self):
        hinst = self.kernel32.GetModuleHandleW(None)
        self._cls_name = f"WHID_Sink_{int(time.time()*1000)}_{threading.get_ident()}"

        self._wnd_proc_ref = WNDPROC(self._wnd_proc)

        wc = WNDCLASSEXW()
        wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
        wc.style = 0
        wc.lpfnWndProc = self._wnd_proc_ref
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = hinst
        wc.hIcon = None
        wc.hCursor = None
        wc.hbrBackground = None
        wc.lpszMenuName = None
        wc.lpszClassName = self._cls_name
        wc.hIconSm = None

        atom = self.user32.RegisterClassExW(ctypes.byref(wc))
        if not atom:
            self.running = False
            return

        self._hwnd = self.user32.CreateWindowExW(
            0,
            self._cls_name,
            "WHID_RawInputSink",
            0,
            0,
            0,
            0,
            0,
            HWND_MESSAGE,
            None,
            hinst,
            None,
        )
        if not self._hwnd:
            self.running = False
            return

        rid = RAWINPUTDEVICE(0x01, 0x06, RIDEV_INPUTSINK, self._hwnd)
        self.user32.RegisterRawInputDevices(
            ctypes.byref(rid),
            1,
            ctypes.sizeof(RAWINPUTDEVICE),
        )

        msg = MSG()
        while self.running:
            b_ret = self.user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if b_ret <= 0:
                break
            self.user32.TranslateMessage(ctypes.byref(msg))
            self.user32.DispatchMessageW(ctypes.byref(msg))

        # Cleanup unregister
        try:
            rid_remove = RAWINPUTDEVICE(0x01, 0x06, RIDEV_REMOVE, None)
            self.user32.RegisterRawInputDevices(
                ctypes.byref(rid_remove),
                1,
                ctypes.sizeof(RAWINPUTDEVICE),
            )
            if self._hwnd:
                self.user32.DestroyWindow(self._hwnd)
        except Exception:
            pass
        self.running = False
