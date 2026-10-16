#!/usr/bin/env bash
"""FloatPen - Floating Desktop Marker and Screen Annotation Tool for Linux."""

import os
import sys

# Ensure X11/XWayland backend for reliable click-through and always-on-top overlay
if "GDK_BACKEND" not in os.environ and os.environ.get("WAYLAND_DISPLAY"):
    os.environ["GDK_BACKEND"] = "x11"

# Add package directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from floatpen.app import FloatPenApp


def main():
    app = FloatPenApp()
    app.run()


if __name__ == "__main__":
    main()
