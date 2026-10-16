"""Floating, draggable, collapsible vertical toolbar for EpicMarker."""

import math
import cairo
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from floatpen.icons import IconWidget, hex_to_rgba


class ColorSwatch(Gtk.DrawingArea):
    """Circular color swatch with selected ring highlight."""
    def __init__(self, hex_color, on_click=None, size=20):
        super().__init__()
        self.hex_color = hex_color
        self.is_selected = False
        self.size = size
        self.on_click = on_click
        self.set_size_request(size + 4, size + 4)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("draw", self._on_draw)
        self.connect("button-press-event", self._on_press)

    def set_selected(self, selected):
        self.is_selected = selected
        self.queue_draw()

    def _on_press(self, widget, event):
        if event.button == 1 and self.on_click:
            self.on_click(self.hex_color)
            return True
        return False

    def _on_draw(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        cx, cy = w / 2.0, h / 2.0
        r = self.size / 2.0

        rgba = hex_to_rgba(self.hex_color)
        cr.set_source_rgba(rgba[0], rgba[1], rgba[2], 1.0)
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.fill_preserve()

        # Outline
        cr.set_source_rgba(1, 1, 1, 0.25)
        cr.set_line_width(1.0)
        cr.stroke()

        if self.is_selected:
            # Active selection ring
            cr.set_source_rgba(1, 1, 1, 0.95)
            cr.set_line_width(2.0)
            cr.arc(cx, cy, r + 2.0, 0, 2 * math.pi)
            cr.stroke()

        return False


class WidthDot(Gtk.DrawingArea):
    """Visual dot indicator for stroke thickness."""
    def __init__(self, width, on_click=None, size=24):
        super().__init__()
        self.width_val = width
        self.is_selected = False
        self.size = size
        self.on_click = on_click
        self.set_size_request(size, size)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("draw", self._on_draw)
        self.connect("button-press-event", self._on_press)

    def set_selected(self, selected):
        self.is_selected = selected
        self.queue_draw()

    def _on_press(self, widget, event):
        if event.button == 1 and self.on_click:
            self.on_click(self.width_val)
            return True
        return False

    def _on_draw(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        cx, cy = w / 2.0, h / 2.0

        # Dot radius proportional to width
        dot_r = max(2.0, min(8.0, self.width_val * 0.45))
        if self.is_selected:
            cr.set_source_rgba(0.23, 0.51, 0.96, 1.0)  # Blue
            cr.arc(cx, cy, dot_r + 2.5, 0, 2 * math.pi)
            cr.stroke()
            cr.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        else:
            cr.set_source_rgba(0.7, 0.7, 0.75, 0.8)

        cr.arc(cx, cy, dot_r, 0, 2 * math.pi)
        cr.fill()
        return False


class ToolbarWindow(Gtk.Window):
    def __init__(self, config, canvas):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.config = config
        self.canvas = canvas

        self.collapsed = config.get("collapsed", False)
        self.drag_start = None
        self.win_start = None

        self.tool_buttons = {}
        self.swatches = []
        self.width_dots = []

        self._setup_window()
        self._build_ui()
        self._load_position()

    def _setup_window(self):
        self.set_title("FloatPen")
        self.set_role("floatpen-toolbar")
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_transient_for(self.canvas)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_MASK
        )

        self.connect("draw", self._on_window_draw)
        self.connect("button-press-event", self._on_mouse_press)
        self.connect("button-release-event", self._on_mouse_release)
        self.connect("motion-notify-event", self._on_mouse_motion)

    def _on_window_draw(self, widget, cr):
        # Draw translucent rounded rectangle
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()

        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        r = 16.0

        cr.set_operator(cairo.OPERATOR_OVER)
        # Deep dark zinc
        cr.set_source_rgba(0.094, 0.094, 0.106, 0.95)
        cr.new_sub_path()
        cr.arc(w - r, r, r, -math.pi / 2, 0)
        cr.arc(w - r, h - r, r, 0, math.pi / 2)
        cr.arc(r, h - r, r, math.pi / 2, math.pi)
        cr.arc(r, r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()
        cr.fill_preserve()

        # Border
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.14)
        cr.set_line_width(1.0)
        cr.stroke()
        return False

    def _load_position(self):
        x = self.config.get("toolbar_x", 30)
        y = self.config.get("toolbar_y", 80)
        self.move(int(x), int(y))

    def _save_position(self):
        pos = self.get_position()
        self.config.set("toolbar_x", pos[0])
        self.config.set("toolbar_y", pos[1])

    def _build_ui(self):
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.main_box.get_style_context().add_class("toolbar-container")
        self.add(self.main_box)

        # 1. Header (Grip handle, Collapse button, Close button)
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        header_box.get_style_context().add_class("drag-grip")

        self.grip_widget = IconWidget("grip", size=16, color="#71717a")
        header_box.pack_start(self.grip_widget, True, True, 2)

        # Collapse toggle
        collapse_btn = Gtk.Button()
        collapse_btn.get_style_context().add_class("action-btn")
        self.collapse_icon = IconWidget("chevron_up" if not self.collapsed else "chevron_down", size=14, color="#a1a1aa")
        collapse_btn.add(self.collapse_icon)
        collapse_btn.set_tooltip_text("Collapse/Expand Toolbar")
        collapse_btn.connect("clicked", self._on_toggle_collapse)
        header_box.pack_start(collapse_btn, False, False, 0)

        # Close button
        close_btn = Gtk.Button()
        close_btn.get_style_context().add_class("action-btn")
        close_btn.get_style_context().add_class("danger")
        close_btn.add(IconWidget("close", size=14, color="#a1a1aa"))
        close_btn.set_tooltip_text("Exit EpicMarker")
        close_btn.connect("clicked", lambda b: Gtk.main_quit())
        header_box.pack_start(close_btn, False, False, 0)

        self.main_box.pack_start(header_box, False, False, 2)

        # 2. Mode Switcher (Always visible even when collapsed)
        self.mode_btn = Gtk.Button()
        self.mode_btn.get_style_context().add_class("mode-btn")
        self.mode_icon = IconWidget("pointer" if self.canvas.mode == "pointer" else "pen", size=22, color="#34d399")
        self.mode_btn.add(self.mode_icon)
        self.mode_btn.connect("clicked", lambda b: self.canvas.toggle_mode())
        self._update_mode_button_style(self.canvas.mode)
        self.main_box.pack_start(self.mode_btn, False, False, 2)

        # 3. Expandable Body Box
        self.body_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.main_box.pack_start(self.body_box, False, False, 0)

        self._build_tools_section()
        self._build_colors_section()
        self._build_width_section()
        self._build_actions_section()

        if self.collapsed:
            self.body_box.hide()

    def _build_tools_section(self):
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.get_style_context().add_class("tool-sep")
        self.body_box.pack_start(sep, False, False, 3)

        tools = [
            ("pen", "Pen Tool [P]", "pen"),
            ("highlighter", "Highlighter Tool [H]", "highlighter"),
            ("eraser", "Eraser Tool [E]", "eraser"),
            ("arrow", "Arrow Tool [A]", "arrow"),
            ("line", "Line Tool [L]", "line"),
            ("rect", "Rectangle Tool [R]", "rect"),
            ("circle", "Circle Tool [C]", "circle"),
            ("text", "Text Tool [T]", "text"),
        ]

        active_tool = self.canvas.active_tool
        for tool_id, tooltip, icon_name in tools:
            btn = Gtk.Button()
            btn.get_style_context().add_class("tool-btn")
            btn.set_tooltip_text(tooltip)
            icon = IconWidget(icon_name, size=20, color="#f4f4f5" if tool_id == active_tool else "#a1a1aa")
            btn.add(icon)
            btn.connect("clicked", lambda b, tid=tool_id: self._on_select_tool(tid))
            if tool_id == active_tool:
                btn.get_style_context().add_class("active")
            self.tool_buttons[tool_id] = (btn, icon)
            self.body_box.pack_start(btn, False, False, 1)

    def _build_colors_section(self):
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.get_style_context().add_class("tool-sep")
        self.body_box.pack_start(sep, False, False, 3)

        # Palette in 2 columns
        grid = Gtk.Grid()
        grid.set_column_spacing(4)
        grid.set_row_spacing(4)
        grid.set_halign(Gtk.Align.CENTER)

        palette = self.config.get("palette", [
            "#ef4444", "#f97316", "#f59e0b", "#10b981",
            "#3b82f6", "#8b5cf6", "#ffffff", "#1e293b"
        ])

        active_color = self.canvas.active_color
        for idx, hex_color in enumerate(palette):
            swatch = ColorSwatch(hex_color, on_click=self._on_select_color, size=18)
            if hex_color.lower() == active_color.lower():
                swatch.set_selected(True)
            self.swatches.append(swatch)
            col = idx % 2
            row = idx // 2
            grid.attach(swatch, col, row, 1, 1)

        self.body_box.pack_start(grid, False, False, 2)

        # Custom color picker button
        pick_btn = Gtk.Button()
        pick_btn.get_style_context().add_class("action-btn")
        pick_btn.set_tooltip_text("Custom Color Picker")
        pick_label = Gtk.Label()
        pick_label.set_markup("<span font='10' color='#71717a'>+ custom</span>")
        pick_btn.add(pick_label)
        pick_btn.connect("clicked", self._open_color_dialog)
        self.body_box.pack_start(pick_btn, False, False, 0)

    def _build_width_section(self):
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.get_style_context().add_class("tool-sep")
        self.body_box.pack_start(sep, False, False, 3)

        widths_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        widths_box.set_halign(Gtk.Align.CENTER)
        widths = [3, 6, 12, 20]
        active_w = self.canvas.active_width

        for w in widths:
            dot = WidthDot(w, on_click=self._on_select_width, size=20)
            if int(w) == int(active_w):
                dot.set_selected(True)
            self.width_dots.append(dot)
            widths_box.pack_start(dot, False, False, 0)

        self.body_box.pack_start(widths_box, False, False, 2)

    def _build_actions_section(self):
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.get_style_context().add_class("tool-sep")
        self.body_box.pack_start(sep, False, False, 3)

        # Board toggle
        self.board_btn = Gtk.Button()
        self.board_btn.get_style_context().add_class("action-btn")
        self.board_icon = IconWidget(f"board_{self.canvas.board_mode}", size=20, color="#a1a1aa")
        self.board_btn.add(self.board_icon)
        self.board_btn.set_tooltip_text(f"Board: {self.canvas.board_mode.title()} (Desktop / Whiteboard / Blackboard) [W/B]")
        self.board_btn.connect("clicked", self._on_cycle_board)
        self.body_box.pack_start(self.board_btn, False, False, 1)

        # Undo
        undo_btn = Gtk.Button()
        undo_btn.get_style_context().add_class("action-btn")
        undo_btn.set_tooltip_text("Undo [Ctrl+Z]")
        undo_btn.add(IconWidget("undo", size=20, color="#a1a1aa"))
        undo_btn.connect("clicked", lambda b: self.canvas.undo())
        self.body_box.pack_start(undo_btn, False, False, 1)

        # Redo
        redo_btn = Gtk.Button()
        redo_btn.get_style_context().add_class("action-btn")
        redo_btn.set_tooltip_text("Redo [Ctrl+Y]")
        redo_btn.add(IconWidget("redo", size=20, color="#a1a1aa"))
        redo_btn.connect("clicked", lambda b: self.canvas.redo())
        self.body_box.pack_start(redo_btn, False, False, 1)

        # Visibility (Eye)
        self.eye_btn = Gtk.Button()
        self.eye_btn.get_style_context().add_class("action-btn")
        self.eye_btn.set_tooltip_text("Hide / Show Drawings")
        self.eye_icon = IconWidget("eye", size=20, color="#a1a1aa")
        self.eye_btn.add(self.eye_icon)
        self.eye_btn.connect("clicked", self._on_toggle_eye)
        self.body_box.pack_start(self.eye_btn, False, False, 1)

        # Clear All (Trash)
        trash_btn = Gtk.Button()
        trash_btn.get_style_context().add_class("action-btn")
        trash_btn.get_style_context().add_class("danger")
        trash_btn.set_tooltip_text("Clear All [Ctrl+K]")
        trash_btn.add(IconWidget("trash", size=20, color="#a1a1aa"))
        trash_btn.connect("clicked", lambda b: self.canvas.clear_canvas())
        self.body_box.pack_start(trash_btn, False, False, 1)

        # Screenshot / Save
        save_btn = Gtk.Button()
        save_btn.get_style_context().add_class("action-btn")
        save_btn.set_tooltip_text("Save Screenshot & Copy [Ctrl+S]")
        save_btn.add(IconWidget("camera", size=20, color="#a1a1aa"))
        save_btn.connect("clicked", self._on_screenshot)
        self.body_box.pack_start(save_btn, False, False, 1)

    def _on_select_tool(self, tool_id):
        self.canvas.set_tool(tool_id)
        for tid, (btn, icon) in self.tool_buttons.items():
            if tid == tool_id:
                btn.get_style_context().add_class("active")
                icon.set_color("#ffffff")
            else:
                btn.get_style_context().remove_class("active")
                icon.set_color("#a1a1aa")

    def _on_select_color(self, hex_color):
        self.canvas.set_color(hex_color)
        for s in self.swatches:
            s.set_selected(s.hex_color.lower() == hex_color.lower())

    def _open_color_dialog(self, widget):
        dialog = Gtk.ColorChooserDialog(title="Choose Custom Color", transient_for=self)
        dialog.set_use_alpha(False)
        curr_rgba = Gdk.RGBA()
        curr_rgba.parse(self.canvas.active_color)
        dialog.set_rgba(curr_rgba)

        if dialog.run() == Gtk.ResponseType.OK:
            rgba = dialog.get_rgba()
            hex_color = f"#{int(rgba.red * 255):02x}{int(rgba.green * 255):02x}{int(rgba.blue * 255):02x}"
            self._on_select_color(hex_color)
        dialog.destroy()

    def _on_select_width(self, width):
        self.canvas.set_width(width)
        for dot in self.width_dots:
            dot.set_selected(int(dot.width_val) == int(width))

    def _on_cycle_board(self, widget):
        new_mode = self.canvas.cycle_board_mode()
        self.board_icon.set_icon(f"board_{new_mode}")
        self.board_btn.set_tooltip_text(f"Board: {new_mode.title()} (Desktop / Whiteboard / Blackboard) [W/B]")

    def _on_toggle_eye(self, widget):
        is_hidden = self.canvas.toggle_hidden()
        self.eye_icon.set_icon("eye_hidden" if is_hidden else "eye")
        self.eye_icon.set_color("#ef4444" if is_hidden else "#a1a1aa")

    def _on_screenshot(self, widget):
        path = self.canvas.save_screenshot()
        self.show_toast(f"Saved: {path}\nCopied to clipboard!")

    def _on_toggle_collapse(self, widget):
        self.collapsed = not self.collapsed
        self.config.set("collapsed", self.collapsed)
        if self.collapsed:
            self.body_box.hide()
            self.collapse_icon.set_icon("chevron_down")
            self.main_box.get_style_context().add_class("toolbar-collapsed")
        else:
            self.body_box.show()
            self.collapse_icon.set_icon("chevron_up")
            self.main_box.get_style_context().remove_class("toolbar-collapsed")
        self.resize(1, 1)

    def on_mode_changed(self, mode):
        self._update_mode_button_style(mode)

    def _update_mode_button_style(self, mode):
        ctx = self.mode_btn.get_style_context()
        if mode == "pointer":
            ctx.remove_class("draw-active")
            ctx.add_class("pointer-active")
            self.mode_icon.set_icon("pointer")
            self.mode_icon.set_color("#34d399")
            self.mode_btn.set_tooltip_text("Pointer Mode: Click-through active (Alt+D / Esc)")
        else:
            ctx.remove_class("pointer-active")
            ctx.add_class("draw-active")
            self.mode_icon.set_icon("pen")
            self.mode_icon.set_color("#60a5fa")
            self.mode_btn.set_tooltip_text("Draw Mode: Drawing on screen (Alt+D)")

    def _on_mouse_press(self, widget, event):
        if event.button == 1:
            self.drag_start = (event.x_root, event.y_root)
            self.win_start = self.get_position()
            return True
        return False

    def _on_mouse_motion(self, widget, event):
        if self.drag_start and self.win_start:
            dx = event.x_root - self.drag_start[0]
            dy = event.y_root - self.drag_start[1]
            self.move(int(self.win_start[0] + dx), int(self.win_start[1] + dy))
            return True
        return False

    def _on_mouse_release(self, widget, event):
        if event.button == 1:
            if self.drag_start:
                self.drag_start = None
                self.win_start = None
                self._save_position()
            return True
        return False

    def show_toast(self, message):
        toast = Gtk.Window(type=Gtk.WindowType.POPUP)
        toast.set_transient_for(self)
        toast.set_decorated(False)
        toast.set_app_paintable(True)
        toast.set_keep_above(True)

        lbl = Gtk.Label(label=message)
        lbl.get_style_context().add_class("toast-window")
        toast.add(lbl)

        # Place toast near toolbar
        tx, ty = self.get_position()
        toast.move(tx + 60, ty + 20)
        toast.show_all()

        GLib.timeout_add(2500, lambda: toast.destroy())
