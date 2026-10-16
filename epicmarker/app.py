"""Main application coordinator for EpicMarker."""

import os
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from epicmarker.config import Config
from epicmarker.canvas import CanvasWindow
from epicmarker.toolbar import ToolbarWindow
from epicmarker.hotkeys import GlobalHotkeyManager


class EpicMarkerApp:
    def __init__(self):
        self.config = Config()
        self._load_styles()

        # Canvas overlay
        self.canvas = CanvasWindow(self.config, on_mode_change=self._on_mode_change)

        # Floating toolbar
        self.toolbar = ToolbarWindow(self.config, self.canvas)

        # Global hotkey manager (Ctrl+Shift+A, Alt+D, F8)
        self.hotkeys = GlobalHotkeyManager(on_toggle_mode=self.canvas.toggle_mode)

    def _load_styles(self):
        css_file = os.path.join(os.path.dirname(__file__), "styles.css")
        if os.path.exists(css_file):
            provider = Gtk.CssProvider()
            provider.load_from_path(css_file)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

    def _on_mode_change(self, mode):
        self.toolbar.on_mode_changed(mode)

    def run(self):
        # Register SIGINT / SIGTERM for clean exit
        signal.signal(signal.SIGINT, lambda sig, frame: GLib.idle_add(Gtk.main_quit))
        signal.signal(signal.SIGTERM, lambda sig, frame: GLib.idle_add(Gtk.main_quit))

        self.canvas.show_all()
        self.toolbar.show_all()
        self.hotkeys.start()

        print("[EpicMarker] Application started.")
        print("  - Toggle Draw/Pointer: Alt+D, Ctrl+Shift+A, or toolbar button")
        print("  - Exit: Click 'X' on toolbar or Ctrl+C")
        try:
            Gtk.main()
        finally:
            self.hotkeys.stop()
