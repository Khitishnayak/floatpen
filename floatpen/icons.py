"""Vector Cairo icon renderers for EpicMarker UI."""

import math
import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c * 2 for c in hex_code])
    if len(hex_code) == 6:
        r = int(hex_code[0:2], 16) / 255.0
        g = int(hex_code[2:4], 16) / 255.0
        b = int(hex_code[4:6], 16) / 255.0
        return (r, g, b, alpha)
    return (1.0, 1.0, 1.0, alpha)


def set_source(cr, color):
    if isinstance(color, str):
        cr.set_source_rgba(*hex_to_rgba(color))
    elif len(color) == 3:
        cr.set_source_rgba(color[0], color[1], color[2], 1.0)
    else:
        cr.set_source_rgba(*color)


def draw_grip(cr, cx, cy, size, color):
    """Draws a 6-dot grip handle (2 columns x 3 rows)."""
    set_source(cr, color)
    dot_r = 1.3
    dx = 4.0
    dy = 4.0
    for col in (-1, 1):
        for row in (-1, 0, 1):
            x = cx + col * (dx / 2.0)
            y = cy + row * dy
            cr.arc(x, y, dot_r, 0, 2 * math.pi)
            cr.fill()


def draw_close(cr, cx, cy, size, color):
    """Draws a clean close 'X'."""
    set_source(cr, color)
    cr.set_line_width(1.8)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    r = size * 0.32
    cr.move_to(cx - r, cy - r)
    cr.line_to(cx + r, cy + r)
    cr.move_to(cx + r, cy - r)
    cr.line_to(cx - r, cy + r)
    cr.stroke()


def draw_chevron(cr, cx, cy, size, color, up=True):
    """Draws a clean minimize/expand chevron."""
    set_source(cr, color)
    cr.set_line_width(1.8)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    r = size * 0.28
    h = size * 0.16
    if up:
        cr.move_to(cx - r, cy + h)
        cr.line_to(cx, cy - h)
        cr.line_to(cx + r, cy + h)
    else:
        cr.move_to(cx - r, cy - h)
        cr.line_to(cx, cy + h)
        cr.line_to(cx + r, cy - h)
    cr.stroke()


def draw_pointer(cr, cx, cy, size, color):
    """Draws a classic cursor pointer arrow."""
    set_source(cr, color)
    cr.set_line_width(1.6)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    s = size * 0.42
    # Arrow tip at top-left
    ox = cx - s * 0.6
    oy = cy - s * 0.7
    cr.move_to(ox, oy)
    cr.line_to(ox, oy + s * 1.5)
    cr.line_to(ox + s * 0.45, oy + s * 1.1)
    cr.line_to(ox + s * 0.85, oy + s * 1.6)
    cr.line_to(ox + s * 1.15, oy + s * 1.4)
    cr.line_to(ox + s * 0.72, oy + s * 0.92)
    cr.line_to(ox + s * 1.25, oy + s * 0.92)
    cr.close_path()
    cr.fill_preserve()
    cr.stroke()


def draw_pen(cr, cx, cy, size, color):
    """Draws a sharp pencil / pen."""
    set_source(cr, color)
    cr.set_line_width(1.6)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    s = size * 0.38
    # Rotate 45 degrees
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(-math.pi / 4)
    # Pencil body
    w = s * 0.4
    h = s * 1.4
    cr.rectangle(-w / 2, -h / 2, w, h * 0.75)
    cr.stroke()
    # Pencil tip
    cr.move_to(-w / 2, h / 2 * 0.5)
    cr.line_to(0, h / 2 + s * 0.25)
    cr.line_to(w / 2, h / 2 * 0.5)
    cr.close_path()
    cr.fill()
    # Eraser band
    cr.rectangle(-w / 2, -h / 2 - s * 0.25, w, s * 0.25)
    cr.fill()
    cr.restore()


def draw_highlighter(cr, cx, cy, size, color):
    """Draws a wide chisel-tip highlighter."""
    set_source(cr, color)
    cr.set_line_width(1.6)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    s = size * 0.38
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(-math.pi / 4)
    w = s * 0.65
    h = s * 1.1
    # Body
    cr.rectangle(-w / 2, -h / 2, w, h * 0.7)
    cr.stroke()
    # Chisel tip
    cr.move_to(-w / 2, h * 0.2)
    cr.line_to(-w * 0.2, h * 0.65)
    cr.line_to(w / 2, h * 0.45)
    cr.line_to(w / 2, h * 0.2)
    cr.close_path()
    cr.fill()
    cr.restore()


def draw_eraser(cr, cx, cy, size, color):
    """Draws an angled eraser block."""
    set_source(cr, color)
    cr.set_line_width(1.6)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    s = size * 0.38
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(-math.pi / 6)
    w = s * 0.8
    h = s * 1.3
    # Top half (rubber)
    cr.rectangle(-w / 2, -h / 2, w, h * 0.5)
    cr.fill()
    # Bottom half (holder)
    cr.rectangle(-w / 2, 0, w, h * 0.5)
    cr.stroke()
    cr.restore()


def draw_arrow(cr, cx, cy, size, color):
    """Draws a clean directional arrow."""
    set_source(cr, color)
    cr.set_line_width(2.0)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    r = size * 0.35
    # Diagonal shaft from bottom-left to top-right
    x0, y0 = cx - r * 0.9, cy + r * 0.9
    x1, y1 = cx + r * 0.9, cy - r * 0.9
    cr.move_to(x0, y0)
    cr.line_to(x1, y1)
    cr.stroke()
    # Arrow wings
    cr.move_to(x1 - r * 0.9, y1)
    cr.line_to(x1, y1)
    cr.line_to(x1, y1 + r * 0.9)
    cr.stroke()


def draw_line(cr, cx, cy, size, color):
    """Draws a clean diagonal line."""
    set_source(cr, color)
    cr.set_line_width(2.2)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    r = size * 0.35
    cr.move_to(cx - r, cy + r)
    cr.line_to(cx + r, cy - r)
    cr.stroke()


def draw_rect(cr, cx, cy, size, color):
    """Draws a rounded rectangle outline."""
    set_source(cr, color)
    cr.set_line_width(1.8)
    r = size * 0.36
    cr.rectangle(cx - r, cy - r * 0.75, r * 2, r * 1.5)
    cr.stroke()


def draw_circle(cr, cx, cy, size, color):
    """Draws a circle outline."""
    set_source(cr, color)
    cr.set_line_width(1.8)
    r = size * 0.34
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.stroke()


def draw_text(cr, cx, cy, size, color):
    """Draws an uppercase 'T' icon."""
    set_source(cr, color)
    cr.set_line_width(2.2)
    cr.set_line_cap(cairo.LINE_CAP_SQUARE)
    s = size * 0.36
    # Crossbar
    cr.move_to(cx - s, cy - s * 0.9)
    cr.line_to(cx + s, cy - s * 0.9)
    # Stem
    cr.move_to(cx, cy - s * 0.9)
    cr.line_to(cx, cy + s)
    cr.stroke()


def draw_undo(cr, cx, cy, size, color):
    """Draws an undo counter-clockwise curved arrow."""
    set_source(cr, color)
    cr.set_line_width(1.8)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    r = size * 0.32
    # Arc
    cr.arc(cx + r * 0.1, cy + r * 0.2, r * 0.8, -math.pi * 0.85, 0)
    cr.stroke()
    # Arrow tip at arc start
    tip_x = cx + r * 0.1 + r * 0.8 * math.cos(-math.pi * 0.85)
    tip_y = cy + r * 0.2 + r * 0.8 * math.sin(-math.pi * 0.85)
    cr.move_to(tip_x, tip_y - r * 0.5)
    cr.line_to(tip_x, tip_y)
    cr.line_to(tip_x + r * 0.5, tip_y)
    cr.stroke()


def draw_redo(cr, cx, cy, size, color):
    """Draws a redo clockwise curved arrow."""
    set_source(cr, color)
    cr.set_line_width(1.8)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    r = size * 0.32
    # Arc
    cr.arc(cx - r * 0.1, cy + r * 0.2, r * 0.8, -math.pi, -math.pi * 0.15)
    cr.stroke()
    # Arrow tip
    tip_x = cx - r * 0.1 + r * 0.8 * math.cos(-math.pi * 0.15)
    tip_y = cy + r * 0.2 + r * 0.8 * math.sin(-math.pi * 0.15)
    cr.move_to(tip_x, tip_y - r * 0.5)
    cr.line_to(tip_x, tip_y)
    cr.line_to(tip_x - r * 0.5, tip_y)
    cr.stroke()


def draw_eye(cr, cx, cy, size, color, hidden=False):
    """Draws an eye icon, with a slash if hidden."""
    set_source(cr, color)
    cr.set_line_width(1.7)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    r = size * 0.38
    # Eye shape
    cr.move_to(cx - r, cy)
    cr.curve_to(cx - r * 0.5, cy - r * 0.65, cx + r * 0.5, cy - r * 0.65, cx + r, cy)
    cr.curve_to(cx + r * 0.5, cy + r * 0.65, cx - r * 0.5, cy + r * 0.65, cx - r, cy)
    cr.stroke()
    # Pupil
    cr.arc(cx, cy, r * 0.28, 0, 2 * math.pi)
    cr.fill()
    if hidden:
        # Slash
        cr.set_source_rgba(0.9, 0.2, 0.2, 1.0)
        cr.set_line_width(2.0)
        cr.move_to(cx - r * 1.1, cy - r * 0.9)
        cr.line_to(cx + r * 1.1, cy + r * 0.9)
        cr.stroke()


def draw_trash(cr, cx, cy, size, color):
    """Draws a clean trash can."""
    set_source(cr, color)
    cr.set_line_width(1.6)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    r = size * 0.34
    # Lid
    cr.move_to(cx - r * 0.9, cy - r * 0.6)
    cr.line_to(cx + r * 0.9, cy - r * 0.6)
    cr.stroke()
    # Handle
    cr.move_to(cx - r * 0.3, cy - r * 0.6)
    cr.line_to(cx - r * 0.3, cy - r * 0.9)
    cr.line_to(cx + r * 0.3, cy - r * 0.9)
    cr.line_to(cx + r * 0.3, cy - r * 0.6)
    cr.stroke()
    # Body
    cr.move_to(cx - r * 0.7, cy - r * 0.5)
    cr.line_to(cx - r * 0.55, cy + r)
    cr.line_to(cx + r * 0.55, cy + r)
    cr.line_to(cx + r * 0.7, cy - r * 0.5)
    cr.stroke()
    # Ribs
    cr.move_to(cx - r * 0.25, cy - r * 0.2)
    cr.line_to(cx - r * 0.2, cy + r * 0.7)
    cr.move_to(cx + r * 0.25, cy - r * 0.2)
    cr.line_to(cx + r * 0.2, cy + r * 0.7)
    cr.stroke()


def draw_board(cr, cx, cy, size, color, mode='transparent'):
    """Draws a board icon representing Transparent, Whiteboard, or Blackboard."""
    set_source(cr, color)
    cr.set_line_width(1.6)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    r = size * 0.36
    # Monitor / Board frame
    cr.rectangle(cx - r, cy - r * 0.75, r * 2, r * 1.5)
    cr.stroke()
    if mode == 'whiteboard':
        # Solid white fill
        cr.rectangle(cx - r + 2, cy - r * 0.75 + 2, r * 2 - 4, r * 1.5 - 4)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.9)
        cr.fill()
    elif mode == 'blackboard':
        # Dark fill with chalk dot
        cr.rectangle(cx - r + 2, cy - r * 0.75 + 2, r * 2 - 4, r * 1.5 - 4)
        cr.set_source_rgba(0.2, 0.2, 0.25, 0.9)
        cr.fill()
    else:
        # Transparent mesh / grid hint
        cr.set_line_width(1.0)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.4)
        cr.move_to(cx - r, cy)
        cr.line_to(cx + r, cy)
        cr.move_to(cx, cy - r * 0.75)
        cr.line_to(cx, cy + r * 0.75)
        cr.stroke()


def draw_camera(cr, cx, cy, size, color):
    """Draws a camera / snapshot icon."""
    set_source(cr, color)
    cr.set_line_width(1.6)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    r = size * 0.36
    # Camera body
    cr.rectangle(cx - r, cy - r * 0.5, r * 2, r * 1.3)
    cr.stroke()
    # Flash bulb / top bump
    cr.move_to(cx - r * 0.4, cy - r * 0.5)
    cr.line_to(cx - r * 0.25, cy - r * 0.85)
    cr.line_to(cx + r * 0.25, cy - r * 0.85)
    cr.line_to(cx + r * 0.4, cy - r * 0.5)
    cr.stroke()
    # Lens
    cr.arc(cx, cy + r * 0.15, r * 0.38, 0, 2 * math.pi)
    cr.stroke()


class IconWidget(Gtk.DrawingArea):
    """A Gtk DrawingArea that renders a specified vector icon."""
    def __init__(self, icon_name, size=22, color="#e4e4e7"):
        super().__init__()
        self.icon_name = icon_name
        self.size = size
        self.color = color
        self.set_size_request(size, size)
        self.connect("draw", self._on_draw)

    def set_color(self, color):
        self.color = color
        self.queue_draw()

    def set_icon(self, icon_name):
        self.icon_name = icon_name
        self.queue_draw()

    def _on_draw(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        cx = w / 2.0
        cy = h / 2.0
        icon = self.icon_name

        if icon == "grip":
            draw_grip(cr, cx, cy, self.size, self.color)
        elif icon == "close":
            draw_close(cr, cx, cy, self.size, self.color)
        elif icon == "chevron_up":
            draw_chevron(cr, cx, cy, self.size, self.color, up=True)
        elif icon == "chevron_down":
            draw_chevron(cr, cx, cy, self.size, self.color, up=False)
        elif icon == "pointer":
            draw_pointer(cr, cx, cy, self.size, self.color)
        elif icon == "pen":
            draw_pen(cr, cx, cy, self.size, self.color)
        elif icon == "highlighter":
            draw_highlighter(cr, cx, cy, self.size, self.color)
        elif icon == "eraser":
            draw_eraser(cr, cx, cy, self.size, self.color)
        elif icon == "arrow":
            draw_arrow(cr, cx, cy, self.size, self.color)
        elif icon == "line":
            draw_line(cr, cx, cy, self.size, self.color)
        elif icon == "rect":
            draw_rect(cr, cx, cy, self.size, self.color)
        elif icon == "circle":
            draw_circle(cr, cx, cy, self.size, self.color)
        elif icon == "text":
            draw_text(cr, cx, cy, self.size, self.color)
        elif icon == "undo":
            draw_undo(cr, cx, cy, self.size, self.color)
        elif icon == "redo":
            draw_redo(cr, cx, cy, self.size, self.color)
        elif icon == "eye":
            draw_eye(cr, cx, cy, self.size, self.color, hidden=False)
        elif icon == "eye_hidden":
            draw_eye(cr, cx, cy, self.size, self.color, hidden=True)
        elif icon == "trash":
            draw_trash(cr, cx, cy, self.size, self.color)
        elif icon.startswith("board_"):
            mode = icon.replace("board_", "")
            draw_board(cr, cx, cy, self.size, self.color, mode=mode)
        elif icon == "camera":
            draw_camera(cr, cx, cy, self.size, self.color)
        return False
