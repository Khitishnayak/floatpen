"""
Platform Engine for FloatPen.
Manages OS-specific window properties, transparent overlays, and click-through pass-through.

Contributors:
- Linux implementation is fully live and operational.
- macOS and Windows contributors: implement the platform-specific hooks in this file!
"""

import sys
import platform
import logging

logger = logging.getLogger("floatpen.platform")

SYSTEM = platform.system()  # 'Linux', 'Darwin' (macOS), or 'Windows'


def is_linux() -> bool:
    return SYSTEM == "Linux"


def is_macos() -> bool:
    return SYSTEM == "Darwin"


def is_windows() -> bool:
    return SYSTEM == "Windows"


def set_click_through(window, enable: bool) -> bool:
    """
    Enables or disables click-through on the overlay canvas window.

    When enable=True (Pointer Mode):
        The overlay remains visible on screen, but all mouse clicks, drags, and scrolls
        pass through directly to the underlying applications.

    When enable=False (Draw Mode):
        The overlay captures mouse clicks and draws annotations.
    """
    if is_linux():
        # Native Linux GTK3 implementation
        try:
            import cairo
            gdk_win = window.get_window() if hasattr(window, "get_window") else None
            if gdk_win:
                if enable:
                    empty_reg = cairo.Region()
                    gdk_win.input_shape_combine_region(empty_reg, 0, 0)
                else:
                    alloc = window.get_allocation()
                    full_reg = cairo.Region(cairo.RectangleInt(0, 0, alloc.width, alloc.height))
                    gdk_win.input_shape_combine_region(full_reg, 0, 0)
                return True
        except Exception as e:
            logger.error("Linux click-through failed: %s", e)
            return False

    elif is_macos():
        # macOS implementation (Help Wanted - Issue #1)
        # Uses Cocoa NSWindow: [nsWindow setIgnoresMouseEvents:YES/NO]
        try:
            from AppKit import NSApplication
            # Contributor TODO: retrieve underlying NSWindow and toggle:
            # ns_win.setIgnoresMouseEvents_(enable)
            logger.info("macOS click-through set to %s (stub)", enable)
            return True
        except ImportError:
            logger.warning("pyobjc-framework-Cocoa not installed for macOS pass-through")
            return False

    elif is_windows():
        # Windows implementation (Help Wanted - Issue #2)
        # Uses Win32 SetWindowLongPtrW: WS_EX_LAYERED | WS_EX_TRANSPARENT
        try:
            import ctypes
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            # Contributor TODO: retrieve HWND and apply:
            # hwnd = ...
            # style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            # if enable:
            #     ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TRANSPARENT)
            # else:
            #     ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style & ~WS_EX_TRANSPARENT)
            logger.info("Windows click-through set to %s (stub)", enable)
            return True
        except Exception as e:
            logger.error("Windows click-through failed: %s", e)
            return False

    return False
