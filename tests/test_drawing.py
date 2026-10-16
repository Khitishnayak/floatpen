"""Unit tests for EpicMarker vector drawing engine and models."""

import os
import sys
import unittest

# Ensure epicmarker is importable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Set backend before importing GTK
os.environ["GDK_BACKEND"] = "x11"

from epicmarker.models import (
    PenStroke, HighlighterStroke, LineShape, ArrowShape,
    RectangleShape, EllipseShape, TextShape, BatchAction,
    distance_point_to_segment
)


class TestGeometryMath(unittest.TestCase):
    def test_distance_point_to_segment(self):
        # Point right on line
        d = distance_point_to_segment(50, 0, 0, 0, 100, 0)
        self.assertAlmostEqual(d, 0.0)

        # Point perpendicular to line segment
        d = distance_point_to_segment(50, 20, 0, 0, 100, 0)
        self.assertAlmostEqual(d, 20.0)

        # Point past segment endpoint
        d = distance_point_to_segment(120, 0, 0, 0, 100, 0)
        self.assertAlmostEqual(d, 20.0)


class TestDrawingPrimitives(unittest.TestCase):
    def test_pen_stroke_intersects(self):
        pen = PenStroke(color="#ef4444", width=6.0)
        pen.add_point(10, 10)
        pen.add_point(50, 50)
        pen.add_point(100, 100)

        # Near mid-segment
        self.assertTrue(pen.intersects(50, 50, radius=5.0))
        # Far away
        self.assertFalse(pen.intersects(300, 300, radius=5.0))

    def test_highlighter_stroke(self):
        hl = HighlighterStroke(color="#f59e0b", width=6.0)
        hl.add_point(20, 20)
        hl.add_point(80, 20)
        # Should have 0.35 alpha
        self.assertAlmostEqual(hl.color[3], 0.35)
        self.assertTrue(hl.intersects(50, 20, radius=8.0))

    def test_arrow_shape(self):
        arrow = ArrowShape(0, 0, 100, 100, color="#3b82f6", width=6.0)
        self.assertTrue(arrow.intersects(50, 50, radius=10.0))
        self.assertFalse(arrow.intersects(0, 100, radius=5.0))

    def test_rectangle_shape(self):
        rect = RectangleShape(10, 10, 110, 110, color="#10b981", width=4.0)
        # Along top edge
        self.assertTrue(rect.intersects(60, 10, radius=6.0))
        # Along right edge
        self.assertTrue(rect.intersects(110, 60, radius=6.0))
        # Deep in interior (not on border)
        self.assertFalse(rect.intersects(60, 60, radius=2.0))

    def test_text_shape(self):
        text = TextShape(100, 100, "Hello World", color="#ffffff", size=24.0)
        self.assertTrue(text.intersects(120, 110, radius=10.0))
        self.assertFalse(text.intersects(400, 400, radius=10.0))

    def test_batch_action_undo_redo(self):
        items = ["item1", "item2"]
        added = ["item3"]
        removed = ["item1"]

        action = BatchAction(added=added, removed=removed)
        # Apply change
        items.remove("item1")
        items.append("item3")
        self.assertEqual(items, ["item2", "item3"])

        # Undo
        action.undo(items)
        self.assertIn("item1", items)
        self.assertNotIn("item3", items)

        # Redo
        action.redo(items)
        self.assertNotIn("item1", items)
        self.assertIn("item3", items)


if __name__ == "__main__":
    unittest.main()
