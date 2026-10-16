"""Global hotkey listener for EpicMarker using libX11."""

import ctypes
import threading
import gi
gi.require_version('GLib', '2.0')
from gi.repository import GLib

# X11 KeySym definitions
XK_A = 0x0061
XK_a = 0x0061
XK_D = 0x0064
XK_d = 0x0064
XK_F8 = 0xffc5

# X11 Modifiers
ShiftMask = (1 << 0)
ControlMask = (1 << 2)
Mod1Mask = (1 << 3)    # Alt
Mod2Mask = (1 << 4)    # Num Lock
LockMask = (1 << 1)    # Caps Lock

GrabModeAsync = 1
KeyPress = 2


class XKeyEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
        ("root", ctypes.c_ulong),
        ("subwindow", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("x_root", ctypes.c_int),
        ("y_root", ctypes.c_int),
        ("state", ctypes.c_uint),
        ("keycode", ctypes.c_uint),
        ("same_screen", ctypes.c_int),
    ]


class XEvent(ctypes.Union):
    _fields_ = [
        ("type", ctypes.c_int),
        ("xkey", XKeyEvent),
        ("pad", ctypes.c_ulong * 24),
    ]


class GlobalHotkeyManager:
    """Listens for global hotkeys (Ctrl+Shift+A, Alt+D, F8) on X11/XWayland."""

    def __init__(self, on_toggle_mode=None):
        self.on_toggle_mode = on_toggle_mode
        self.running = False
        self.thread = None
        self.disp = None
        self.x11 = None
        self._init_x11()

    def _init_x11(self):
        try:
            self.x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
            self.x11.XOpenDisplay.restype = ctypes.c_void_p
            self.x11.XOpenDisplay.argtypes = [ctypes.c_char_p]

            self.x11.XDefaultRootWindow.restype = ctypes.c_ulong
            self.x11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]

            self.x11.XKeysymToKeycode.restype = ctypes.c_ubyte
            self.x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]

            self.x11.XGrabKey.argtypes = [
                ctypes.c_void_p, ctypes.c_int, ctypes.c_uint,
                ctypes.c_ulong, ctypes.c_int, ctypes.c_int, ctypes.c_int
            ]
            self.x11.XUngrabKey.argtypes = [
                ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_ulong
            ]
            self.x11.XNextEvent.argtypes = [ctypes.c_void_p, ctypes.POINTER(XEvent)]
            self.x11.XCloseDisplay.argtypes = [ctypes.c_void_p]
        except Exception as e:
            print(f"[EpicMarker] Hotkey manager: could not load libX11: {e}")
            self.x11 = None

    def start(self):
        if not self.x11:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        self.disp = self.x11.XOpenDisplay(b":0")
        if not self.disp:
            self.disp = self.x11.XOpenDisplay(None)
        if not self.disp:
            print("[EpicMarker] Hotkey manager: could not open display for global keys.")
            return

        root = self.x11.XDefaultRootWindow(self.disp)

        # Get keycodes
        kc_a = self.x11.XKeysymToKeycode(self.disp, XK_A)
        kc_d = self.x11.XKeysymToKeycode(self.disp, XK_D)
        kc_f8 = self.x11.XKeysymToKeycode(self.disp, XK_F8)

        # Grab combinations (also covering NumLock / CapsLock variants)
        lock_mods = [0, LockMask, Mod2Mask, LockMask | Mod2Mask]

        for mod in lock_mods:
            # Ctrl + Shift + A
            if kc_a:
                self.x11.XGrabKey(self.disp, kc_a, ControlMask | ShiftMask | mod, root, 1, GrabModeAsync, GrabModeAsync)
            # Alt + D
            if kc_d:
                self.x11.XGrabKey(self.disp, kc_d, Mod1Mask | mod, root, 1, GrabModeAsync, GrabModeAsync)
            # F8
            if kc_f8:
                self.x11.XGrabKey(self.disp, kc_f8, mod, root, 1, GrabModeAsync, GrabModeAsync)

        event = XEvent()
        while self.running:
            self.x11.XNextEvent(self.disp, ctypes.byref(event))
            if event.type == KeyPress:
                kc = event.xkey.keycode
                if (kc == kc_a) or (kc == kc_d) or (kc == kc_f8):
                    if self.on_toggle_mode:
                        GLib.idle_add(self.on_toggle_mode)

    def stop(self):
        self.running = False
