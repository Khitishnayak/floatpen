"""Configuration management for EpicMarker."""

import json
import os

DEFAULT_PALETTE = [
    "#ef4444",  # Red
    "#f97316",  # Orange
    "#f59e0b",  # Amber/Yellow
    "#10b981",  # Green
    "#3b82f6",  # Blue
    "#8b5cf6",  # Purple
    "#ffffff",  # White
    "#1e293b",  # Charcoal/Black
]

DEFAULT_CONFIG = {
    "toolbar_x": 30,
    "toolbar_y": 80,
    "active_tool": "pen",
    "active_color": "#ef4444",
    "active_width": 6,
    "board_mode": "transparent",
    "collapsed": False,
    "palette": DEFAULT_PALETTE,
}

CONFIG_DIR = os.path.expanduser("~/.config/epicmarker")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


class Config:
    def __init__(self):
        self.data = dict(DEFAULT_CONFIG)
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    if isinstance(saved, dict):
                        self.data.update(saved)
            except Exception as e:
                print(f"[EpicMarker] Warning: Could not load config: {e}")

    def save(self):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"[EpicMarker] Warning: Could not save config: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
