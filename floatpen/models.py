"""Drawing models and vector primitives for EpicMarker."""

import math
import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo


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


def distance_point_to_segment(px, py, x0, y0, x1, y1):
    """Calculates the Euclidean distance from point (px, py) to line segment (x0, y0)-(x1, y1)."""
    dx = x1 - x0
    dy = y1 - y0
    l2 = dx * dx + dy * dy
    if l2 == 0:
        return math.hypot(px - x0, py - y0)
    t = max(0.0, min(1.0, ((px - x0) * dx + (py - y0) * dy) / l2))
    proj_x = x0 + t * dx
    proj_y = y0 + t * dy
    return math.hypot(px - proj_x, py - proj_y)


class BaseItem:
    def draw(self, cr):
        raise NotImplementedError

    def intersects(self, px, py, radius):
        raise NotImplementedError


class PenStroke(BaseItem):
    def __init__(self, color="#ef4444", width=6.0):
        self.color = color if isinstance(color, tuple) else hex_to_rgba(color)
        self.width = float(width)
        self.points = []

    def add_point(self, x, y):
        self.points.append((float(x), float(y)))

    def draw(self, cr):
        if not self.points:
            return
        cr.save()
        cr.set_source_rgba(*self.color)
        cr.set_line_width(self.width)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)

        n = len(self.points)
        if n == 1:
            x, y = self.points[0]
            cr.arc(x, y, self.width / 2.0, 0, 2 * math.pi)
            cr.fill()
        elif n == 2:
            cr.move_to(self.points[0][0], self.points[0][1])
            cr.line_to(self.points[1][0], self.points[1][1])
            cr.stroke()
        else:
            # Midpoint Bezier smoothing
            cr.move_to(self.points[0][0], self.points[0][1])
            mid0_x = (self.points[0][0] + self.points[1][0]) / 2.0
            mid0_y = (self.points[0][1] + self.points[1][1]) / 2.0
            cr.line_to(mid0_x, mid0_y)

            for i in range(1, n - 1):
                curr_x, curr_y = self.points[i]
                next_x, next_y = self.points[i + 1]
                mid_x = (curr_x + next_x) / 2.0
                mid_y = (curr_y + next_y) / 2.0
                cr.curve_to(curr_x, curr_y, curr_x, curr_y, mid_x, mid_y)

            cr.line_to(self.points[-1][0], self.points[-1][1])
            cr.stroke()
        cr.restore()

    def intersects(self, px, py, radius):
        thresh = radius + (self.width / 2.0)
        n = len(self.points)
        if n == 1:
            return math.hypot(px - self.points[0][0], py - self.points[0][1]) <= thresh
        for i in range(n - 1):
            x0, y0 = self.points[i]
            x1, y1 = self.points[i + 1]
            if distance_point_to_segment(px, py, x0, y0, x1, y1) <= thresh:
                return True
        return False


class HighlighterStroke(BaseItem):
    def __init__(self, color="#f59e0b", width=6.0):
        # Convert color to 0.35 alpha
        rgba = color if isinstance(color, tuple) else hex_to_rgba(color)
        self.color = (rgba[0], rgba[1], rgba[2], 0.35)
        self.width = float(width) * 2.8
        self.points = []

    def add_point(self, x, y):
        self.points.append((float(x), float(y)))

    def draw(self, cr):
        if not self.points:
            return
        cr.save()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_source_rgba(*self.color)
        cr.set_line_width(self.width)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)

        n = len(self.points)
        if n == 1:
            x, y = self.points[0]
            cr.arc(x, y, self.width / 2.0, 0, 2 * math.pi)
            cr.fill()
        elif n == 2:
            cr.move_to(self.points[0][0], self.points[0][1])
            cr.line_to(self.points[1][0], self.points[1][1])
            cr.stroke()
        else:
            cr.move_to(self.points[0][0], self.points[0][1])
            mid0_x = (self.points[0][0] + self.points[1][0]) / 2.0
            mid0_y = (self.points[0][1] + self.points[1][1]) / 2.0
            cr.line_to(mid0_x, mid0_y)

            for i in range(1, n - 1):
                curr_x, curr_y = self.points[i]
                next_x, next_y = self.points[i + 1]
                mid_x = (curr_x + next_x) / 2.0
                mid_y = (curr_y + next_y) / 2.0
                cr.curve_to(curr_x, curr_y, curr_x, curr_y, mid_x, mid_y)

            cr.line_to(self.points[-1][0], self.points[-1][1])
            cr.stroke()
        cr.restore()

    def intersects(self, px, py, radius):
        thresh = radius + (self.width / 2.0)
        n = len(self.points)
        if n == 1:
            return math.hypot(px - self.points[0][0], py - self.points[0][1]) <= thresh
        for i in range(n - 1):
            x0, y0 = self.points[i]
            x1, y1 = self.points[i + 1]
            if distance_point_to_segment(px, py, x0, y0, x1, y1) <= thresh:
                return True
        return False


class LineShape(BaseItem):
    def __init__(self, x0, y0, x1, y1, color="#ef4444", width=6.0):
        self.x0, self.y0 = float(x0), float(y0)
        self.x1, self.y1 = float(x1), float(y1)
        self.color = color if isinstance(color, tuple) else hex_to_rgba(color)
        self.width = float(width)

    def update_end(self, x1, y1, snap=False):
        if snap:
            # Snap angle to 15-degree increments
            dx = x1 - self.x0
            dy = y1 - self.y0
            angle = math.atan2(dy, dx)
            snap_interval = math.pi / 12.0  # 15 degrees
            snapped_angle = round(angle / snap_interval) * snap_interval
            dist = math.hypot(dx, dy)
            self.x1 = self.x0 + dist * math.cos(snapped_angle)
            self.y1 = self.y0 + dist * math.sin(snapped_angle)
        else:
            self.x1, self.y1 = float(x1), float(y1)

    def draw(self, cr):
        cr.save()
        cr.set_source_rgba(*self.color)
        cr.set_line_width(self.width)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(self.x0, self.y0)
        cr.line_to(self.x1, self.y1)
        cr.stroke()
        cr.restore()

    def intersects(self, px, py, radius):
        thresh = radius + (self.width / 2.0)
        return distance_point_to_segment(px, py, self.x0, self.y0, self.x1, self.y1) <= thresh


class ArrowShape(BaseItem):
    def __init__(self, x0, y0, x1, y1, color="#ef4444", width=6.0):
        self.x0, self.y0 = float(x0), float(y0)
        self.x1, self.y1 = float(x1), float(y1)
        self.color = color if isinstance(color, tuple) else hex_to_rgba(color)
        self.width = float(width)

    def update_end(self, x1, y1, snap=False):
        if snap:
            dx = x1 - self.x0
            dy = y1 - self.y0
            angle = math.atan2(dy, dx)
            snap_interval = math.pi / 12.0  # 15 degrees
            snapped_angle = round(angle / snap_interval) * snap_interval
            dist = math.hypot(dx, dy)
            self.x1 = self.x0 + dist * math.cos(snapped_angle)
            self.y1 = self.y0 + dist * math.sin(snapped_angle)
        else:
            self.x1, self.y1 = float(x1), float(y1)

    def draw(self, cr):
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        length = math.hypot(dx, dy)
        if length < 4.0:
            return

        cr.save()
        cr.set_source_rgba(*self.color)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)

        ux = dx / length
        uy = dy / length
        px = -uy
        py = ux

        head_len = min(max(self.width * 4.2, 16.0), length * 0.55)
        head_half_w = head_len * 0.52

        bx = self.x1 - ux * head_len
        by = self.y1 - uy * head_len
        w1_x = bx + px * head_half_w
        w1_y = by + py * head_half_w
        w2_x = bx - px * head_half_w
        w2_y = by - py * head_half_w

        # Draw shaft
        cr.set_line_width(self.width)
        cr.move_to(self.x0, self.y0)
        cr.line_to(bx + ux * (self.width / 2.0), by + uy * (self.width / 2.0))
        cr.stroke()

        # Draw filled head with subtle notch
        cr.move_to(self.x1, self.y1)
        cr.line_to(w1_x, w1_y)
        cr.line_to(bx + ux * (head_len * 0.22), by + uy * (head_len * 0.22))
        cr.line_to(w2_x, w2_y)
        cr.close_path()
        cr.fill()
        cr.restore()

    def intersects(self, px, py, radius):
        thresh = radius + (self.width / 2.0)
        return distance_point_to_segment(px, py, self.x0, self.y0, self.x1, self.y1) <= thresh


class RectangleShape(BaseItem):
    def __init__(self, x0, y0, x1, y1, color="#ef4444", width=6.0):
        self.x0, self.y0 = float(x0), float(y0)
        self.x1, self.y1 = float(x1), float(y1)
        self.color = color if isinstance(color, tuple) else hex_to_rgba(color)
        self.width = float(width)

    def update_end(self, x1, y1, snap=False):
        if snap:
            # Snap to square
            dx = x1 - self.x0
            dy = y1 - self.y0
            s = max(abs(dx), abs(dy))
            self.x1 = self.x0 + math.copysign(s, dx)
            self.y1 = self.y0 + math.copysign(s, dy)
        else:
            self.x1, self.y1 = float(x1), float(y1)

    def draw(self, cr):
        x = min(self.x0, self.x1)
        y = min(self.y0, self.y1)
        w = abs(self.x1 - self.x0)
        h = abs(self.y1 - self.y0)
        if w < 1 or h < 1:
            return

        cr.save()
        cr.set_source_rgba(*self.color)
        cr.set_line_width(self.width)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)

        r = min(8.0, w / 4.0, h / 4.0)
        if r > 1.0:
            # Rounded rectangle
            cr.new_sub_path()
            cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
            cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
            cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
            cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
            cr.close_path()
        else:
            cr.rectangle(x, y, w, h)
        cr.stroke()
        cr.restore()

    def intersects(self, px, py, radius):
        x = min(self.x0, self.x1)
        y = min(self.y0, self.y1)
        w = abs(self.x1 - self.x0)
        h = abs(self.y1 - self.y0)
        thresh = radius + (self.width / 2.0)
        # Check all 4 edges
        d1 = distance_point_to_segment(px, py, x, y, x + w, y)
        d2 = distance_point_to_segment(px, py, x + w, y, x + w, y + h)
        d3 = distance_point_to_segment(px, py, x + w, y + h, x, y + h)
        d4 = distance_point_to_segment(px, py, x, y + h, x, y)
        return min(d1, d2, d3, d4) <= thresh


class EllipseShape(BaseItem):
    def __init__(self, x0, y0, x1, y1, color="#ef4444", width=6.0):
        self.x0, self.y0 = float(x0), float(y0)
        self.x1, self.y1 = float(x1), float(y1)
        self.color = color if isinstance(color, tuple) else hex_to_rgba(color)
        self.width = float(width)

    def update_end(self, x1, y1, snap=False):
        if snap:
            # Snap to circle
            dx = x1 - self.x0
            dy = y1 - self.y0
            s = max(abs(dx), abs(dy))
            self.x1 = self.x0 + math.copysign(s, dx)
            self.y1 = self.y0 + math.copysign(s, dy)
        else:
            self.x1, self.y1 = float(x1), float(y1)

    def draw(self, cr):
        x = min(self.x0, self.x1)
        y = min(self.y0, self.y1)
        w = abs(self.x1 - self.x0)
        h = abs(self.y1 - self.y0)
        if w < 1 or h < 1:
            return

        cx = x + w / 2.0
        cy = y + h / 2.0
        rx = w / 2.0
        ry = h / 2.0

        cr.save()
        cr.set_source_rgba(*self.color)
        cr.set_line_width(self.width)
        cr.translate(cx, cy)
        cr.scale(rx, ry)
        cr.arc(0, 0, 1.0, 0, 2 * math.pi)
        cr.restore()
        cr.stroke()

    def intersects(self, px, py, radius):
        x = min(self.x0, self.x1)
        y = min(self.y0, self.y1)
        w = abs(self.x1 - self.x0)
        h = abs(self.y1 - self.y0)
        if w < 1 or h < 1:
            return False
        cx = x + w / 2.0
        cy = y + h / 2.0
        rx = w / 2.0
        ry = h / 2.0
        # Normalized distance to perimeter
        dx = (px - cx) / max(rx, 1e-4)
        dy = (py - cy) / max(ry, 1e-4)
        dist = math.hypot(dx, dy)
        # Check boundary band
        pixel_dist = abs(dist - 1.0) * min(rx, ry)
        return pixel_dist <= radius + (self.width / 2.0)


class TextShape(BaseItem):
    def __init__(self, x, y, text, color="#ef4444", size=24.0):
        self.x = float(x)
        self.y = float(y)
        self.text = text
        self.color = color if isinstance(color, tuple) else hex_to_rgba(color)
        self.size = float(size)
        self._cached_bounds = (0, 0)

    def draw(self, cr):
        if not self.text:
            return
        cr.save()
        cr.set_source_rgba(*self.color)
        layout = PangoCairo.create_layout(cr)
        layout.set_text(self.text, -1)
        font_desc = Pango.FontDescription(f"Sans Bold {int(self.size)}")
        layout.set_font_description(font_desc)
        pango_w, pango_h = layout.get_pixel_size()
        self._cached_bounds = (pango_w, pango_h)

        cr.move_to(self.x, self.y)
        PangoCairo.show_layout(cr, layout)
        cr.restore()

    def intersects(self, px, py, radius):
        w, h = self._cached_bounds
        if w == 0:
            w = len(self.text) * self.size * 0.6
            h = self.size * 1.3
        return (self.x - radius <= px <= self.x + w + radius) and (self.y - radius <= py <= self.y + h + radius)


class BatchAction:
    """Action wrapper for undoing multiple item additions or removals."""
    def __init__(self, added=None, removed=None):
        self.added = added or []
        self.removed = removed or []

    def undo(self, items_list):
        for item in self.added:
            if item in items_list:
                items_list.remove(item)
        for item in self.removed:
            items_list.append(item)

    def redo(self, items_list):
        for item in self.removed:
            if item in items_list:
                items_list.remove(item)
        for item in self.added:
            items_list.append(item)
