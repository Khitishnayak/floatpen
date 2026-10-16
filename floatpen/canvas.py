"""Fullscreen transparent overlay and drawing canvas for EpicMarker."""

import os
import time
import math
import cairo
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

from floatpen.models import (
    PenStroke, HighlighterStroke, LineShape, ArrowShape,
    RectangleShape, EllipseShape, TextShape
)


class CanvasWindow(Gtk.Window):
    def __init__(self, config, on_mode_change=None):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.config = config
        self.on_mode_change = on_mode_change

        self.screen_x = 0
        self.screen_y = 0
        self.screen_w = 1920
        self.screen_h = 1080

        # State
        self.mode = "pointer"  # "draw" or "pointer"
        self.active_tool = config.get("active_tool", "pen")
        self.active_color = config.get("active_color", "#ef4444")
        self.active_width = float(config.get("active_width", 6))
        self.board_mode = config.get("board_mode", "transparent")
        self.hidden = False

        self.items = []
        self.undo_stack = []
        self.redo_stack = []

        self.current_item = None
        self.current_erased_in_drag = []
        self.text_entry_widget = None
        self.text_entry_pos = (0, 0)

        self._setup_window()
        self._update_geometry()
        self._connect_events()

    def _setup_window(self):
        self.set_title("FloatPen Overlay")
        self.set_role("floatpen-overlay")
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)

        # RGBA visual for transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

    def _update_geometry(self):
        display = Gdk.Display.get_default()
        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        n = display.get_n_monitors()
        for i in range(n):
            mon = display.get_monitor(i)
            geom = mon.get_geometry()
            min_x = min(min_x, geom.x)
            min_y = min(min_y, geom.y)
            max_x = max(max_x, geom.x + geom.width)
            max_y = max(max_y, geom.y + geom.height)

        self.screen_x = min_x
        self.screen_y = min_y
        self.screen_w = max(100, max_x - min_x)
        self.screen_h = max(100, max_y - min_y)

        self.move(self.screen_x, self.screen_y)
        self.set_default_size(self.screen_w, self.screen_h)
        self.resize(self.screen_w, self.screen_h)

    def _connect_events(self):
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_MASK
            | Gdk.EventMask.KEY_PRESS_MASK
            | Gdk.EventMask.KEY_RELEASE_MASK
        )
        self.connect("draw", self._on_draw)
        self.connect("button-press-event", self._on_button_press)
        self.connect("button-release-event", self._on_button_release)
        self.connect("motion-notify-event", self._on_motion_notify)
        self.connect("key-press-event", self._on_key_press)
        self.connect("realize", self._on_realize)

    def _on_realize(self, widget):
        # Update input shape based on initial mode
        if self.mode == "pointer":
            self.apply_pointer_mode()
        else:
            self.apply_draw_mode()

    def set_mode(self, mode):
        """Switches between 'draw' and 'pointer' mode."""
        if self.mode == mode:
            return
        self.mode = mode
        if mode == "pointer":
            self.apply_pointer_mode()
        else:
            self.apply_draw_mode()

        if self.on_mode_change:
            self.on_mode_change(mode)

    def toggle_mode(self):
        new_mode = "pointer" if self.mode == "draw" else "draw"
        self.set_mode(new_mode)

    def apply_pointer_mode(self):
        gdk_win = self.get_window()
        if gdk_win:
            # Set empty region so mouse clicks pass through to underlying windows
            empty_reg = cairo.Region()
            gdk_win.input_shape_combine_region(empty_reg, 0, 0)
            gdk_win.set_cursor(None)
        if self.text_entry_widget:
            self._close_text_entry(commit=False)

    def apply_draw_mode(self):
        gdk_win = self.get_window()
        if gdk_win:
            # Full input region so canvas receives mouse clicks
            full_reg = cairo.Region(cairo.RectangleInt(0, 0, self.screen_w, self.screen_h))
            gdk_win.input_shape_combine_region(full_reg, 0, 0)
            self._update_cursor()

    def _update_cursor(self):
        gdk_win = self.get_window()
        if not gdk_win:
            return
        display = self.get_display()
        if self.mode == "pointer":
            gdk_win.set_cursor(None)
            return

        tool = self.active_tool
        if tool in ("pen", "highlighter", "line", "arrow", "rect", "circle"):
            c = Gdk.Cursor.new_from_name(display, "crosshair")
        elif tool == "text":
            c = Gdk.Cursor.new_from_name(display, "text")
        elif tool == "eraser":
            c = Gdk.Cursor.new_from_name(display, "cell") or Gdk.Cursor.new_from_name(display, "crosshair")
        else:
            c = Gdk.Cursor.new_from_name(display, "default")
        gdk_win.set_cursor(c)

    def set_tool(self, tool_name):
        self.active_tool = tool_name
        self.config.set("active_tool", tool_name)
        if self.mode != "draw":
            self.set_mode("draw")
        else:
            self._update_cursor()

    def set_color(self, hex_color):
        self.active_color = hex_color
        self.config.set("active_color", hex_color)

    def set_width(self, width):
        self.active_width = float(width)
        self.config.set("active_width", self.active_width)

    def set_board_mode(self, mode):
        self.board_mode = mode
        self.config.set("board_mode", mode)
        self.queue_draw()

    def cycle_board_mode(self):
        modes = ["transparent", "whiteboard", "blackboard"]
        idx = (modes.index(self.board_mode) + 1) % len(modes) if self.board_mode in modes else 0
        self.set_board_mode(modes[idx])
        return modes[idx]

    def toggle_hidden(self):
        self.hidden = not self.hidden
        self.queue_draw()
        return self.hidden

    def _on_draw(self, widget, cr):
        # 1. Background
        if self.board_mode == "transparent":
            cr.set_operator(cairo.OPERATOR_SOURCE)
            cr.set_source_rgba(0, 0, 0, 0)
            cr.paint()
        elif self.board_mode == "whiteboard":
            cr.set_operator(cairo.OPERATOR_SOURCE)
            cr.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            cr.paint()
        elif self.board_mode == "blackboard":
            cr.set_operator(cairo.OPERATOR_SOURCE)
            cr.set_source_rgba(0.094, 0.094, 0.106, 1.0)
            cr.paint()

        cr.set_operator(cairo.OPERATOR_OVER)

        # 2. Drawings
        if not self.hidden:
            for item in self.items:
                item.draw(cr)

            if self.current_item:
                self.current_item.draw(cr)

        return False

    def _on_button_press(self, widget, event):
        if self.mode != "draw":
            return False

        # Right click toggles back to pointer mode or cancels shape
        if event.button == 3:
            if self.current_item:
                self.current_item = None
                self.queue_draw()
            else:
                self.set_mode("pointer")
            return True

        if event.button != 1:
            return False

        x, y = event.x, event.y
        tool = self.active_tool

        if tool == "pen":
            self.current_item = PenStroke(color=self.active_color, width=self.active_width)
            self.current_item.add_point(x, y)
            self.queue_draw()
        elif tool == "highlighter":
            self.current_item = HighlighterStroke(color=self.active_color, width=self.active_width)
            self.current_item.add_point(x, y)
            self.queue_draw()
        elif tool == "line":
            self.current_item = LineShape(x, y, x, y, color=self.active_color, width=self.active_width)
            self.queue_draw()
        elif tool == "arrow":
            self.current_item = ArrowShape(x, y, x, y, color=self.active_color, width=self.active_width)
            self.queue_draw()
        elif tool == "rect":
            self.current_item = RectangleShape(x, y, x, y, color=self.active_color, width=self.active_width)
            self.queue_draw()
        elif tool == "circle":
            self.current_item = EllipseShape(x, y, x, y, color=self.active_color, width=self.active_width)
            self.queue_draw()
        elif tool == "eraser":
            self.current_erased_in_drag = []
            self.erase_at(x, y, radius=18.0)
        elif tool == "text":
            self._open_text_entry(x, y)

        return True

    def _on_motion_notify(self, widget, event):
        if self.mode != "draw":
            return False

        x, y = event.x, event.y
        snap = bool(event.state & Gdk.ModifierType.SHIFT_MASK)

        if self.current_item:
            tool = self.active_tool
            if tool in ("pen", "highlighter"):
                self.current_item.add_point(x, y)
                self.queue_draw()
            elif tool in ("line", "arrow", "rect", "circle"):
                self.current_item.update_end(x, y, snap=snap)
                self.queue_draw()

        elif self.active_tool == "eraser" and (event.state & Gdk.ModifierType.BUTTON1_MASK):
            self.erase_at(x, y, radius=18.0)

        return True

    def _on_button_release(self, widget, event):
        if self.mode != "draw":
            return False

        if event.button == 1:
            if self.current_item:
                self.items.append(self.current_item)
                self.undo_stack.append(("add", self.current_item))
                self.redo_stack.clear()
                self.current_item = None
                self.queue_draw()
            elif self.active_tool == "eraser":
                if self.current_erased_in_drag:
                    self.undo_stack.append(("erase_batch", list(self.current_erased_in_drag)))
                    self.redo_stack.clear()
                    self.current_erased_in_drag = []

        return True

    def erase_at(self, px, py, radius=18.0):
        erased_now = []
        for item in list(self.items):
            if item.intersects(px, py, radius):
                self.items.remove(item)
                erased_now.append(item)
                if item not in self.current_erased_in_drag:
                    self.current_erased_in_drag.append(item)
        if erased_now:
            self.queue_draw()

    def _open_text_entry(self, x, y):
        self._close_text_entry(commit=True)
        self.text_entry_pos = (x, y)

        entry_win = Gtk.Window(type=Gtk.WindowType.POPUP)
        entry_win.set_transient_for(self)
        entry_win.set_keep_above(True)
        entry_win.set_decorated(False)
        entry_win.set_app_paintable(True)

        entry = Gtk.Entry()
        entry.get_style_context().add_class("canvas-text-entry")
        entry.set_placeholder_text("Type text here... (Enter to finish, Esc to cancel)")
        entry.connect("activate", lambda e: self._close_text_entry(commit=True))
        entry.connect("key-press-event", self._on_text_entry_key)

        entry_win.add(entry)
        entry_win.move(int(x), int(y))
        entry_win.show_all()
        entry.grab_focus()

        self.text_entry_widget = entry_win
        self.text_entry_input = entry

    def _on_text_entry_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self._close_text_entry(commit=False)
            return True
        return False

    def _close_text_entry(self, commit=True):
        if not self.text_entry_widget:
            return
        if commit:
            text = self.text_entry_input.get_text().strip()
            if text:
                x, y = self.text_entry_pos
                font_size = max(18.0, self.active_width * 3.5)
                text_item = TextShape(x, y, text, color=self.active_color, size=font_size)
                self.items.append(text_item)
                self.undo_stack.append(("add", text_item))
                self.redo_stack.clear()
                self.queue_draw()

        self.text_entry_widget.destroy()
        self.text_entry_widget = None
        self.text_entry_input = None

    def undo(self):
        if not self.undo_stack:
            return
        action, payload = self.undo_stack.pop()
        if action == "add":
            if payload in self.items:
                self.items.remove(payload)
                self.redo_stack.append(("add", payload))
        elif action == "erase_batch":
            for item in payload:
                self.items.append(item)
            self.redo_stack.append(("erase_batch", payload))
        elif action == "clear":
            self.items.extend(payload)
            self.redo_stack.append(("clear", payload))
        self.queue_draw()

    def redo(self):
        if not self.redo_stack:
            return
        action, payload = self.redo_stack.pop()
        if action == "add":
            self.items.append(payload)
            self.undo_stack.append(("add", payload))
        elif action == "erase_batch":
            for item in payload:
                if item in self.items:
                    self.items.remove(item)
            self.undo_stack.append(("erase_batch", payload))
        elif action == "clear":
            self.items.clear()
            self.undo_stack.append(("clear", payload))
        self.queue_draw()

    def clear_canvas(self):
        if not self.items:
            return
        self.undo_stack.append(("clear", list(self.items)))
        self.redo_stack.clear()
        self.items.clear()
        self.queue_draw()

    def _on_key_press(self, widget, event):
        keyval = event.keyval
        ctrl = bool(event.state & Gdk.ModifierType.CONTROL_MASK)

        if keyval == Gdk.KEY_Escape:
            self.set_mode("pointer")
            return True

        if ctrl:
            if keyval in (Gdk.KEY_z, Gdk.KEY_Z):
                self.undo()
                return True
            elif keyval in (Gdk.KEY_y, Gdk.KEY_Y):
                self.redo()
                return True
            elif keyval in (Gdk.KEY_k, Gdk.KEY_K):
                self.clear_canvas()
                return True
            elif keyval in (Gdk.KEY_s, Gdk.KEY_S):
                self.save_screenshot()
                return True

        # Tool shortcuts
        key_char = chr(keyval).lower() if 32 <= keyval <= 126 else ""
        if key_char == "p":
            self.set_tool("pen")
            return True
        elif key_char == "h":
            self.set_tool("highlighter")
            return True
        elif key_char == "e":
            self.set_tool("eraser")
            return True
        elif key_char == "a":
            self.set_tool("arrow")
            return True
        elif key_char == "l":
            self.set_tool("line")
            return True
        elif key_char == "r":
            self.set_tool("rect")
            return True
        elif key_char == "c":
            self.set_tool("circle")
            return True
        elif key_char == "t":
            self.set_tool("text")
            return True
        elif key_char == "w":
            self.set_board_mode("whiteboard")
            return True
        elif key_char == "b":
            self.set_board_mode("blackboard")
            return True

        return False

    def save_screenshot(self):
        """Renders the canvas drawing and saves it to ~/Pictures/Screenshots + Clipboard."""
        shot_dir = os.path.expanduser("~/Pictures/Screenshots")
        os.makedirs(shot_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"floatpen_{timestamp}.png"
        filepath = os.path.join(shot_dir, filename)

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.screen_w, self.screen_h)
        cr = cairo.Context(surface)

        # Background
        if self.board_mode == "whiteboard":
            cr.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            cr.paint()
        elif self.board_mode == "blackboard":
            cr.set_source_rgba(0.094, 0.094, 0.106, 1.0)
            cr.paint()
        else:
            cr.set_source_rgba(0, 0, 0, 0)
            cr.paint()

        cr.set_operator(cairo.OPERATOR_OVER)
        for item in self.items:
            item.draw(cr)

        surface.write_to_png(filepath)

        # Copy to clipboard
        try:
            pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, self.screen_w, self.screen_h)
            clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clip.set_image(pixbuf)
            clip.store()
        except Exception as e:
            print(f"[EpicMarker] Clipboard error: {e}")

        return filepath
