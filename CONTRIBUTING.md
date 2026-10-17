# Contributing to FloatPen 🖊️

Thank you for your interest in contributing to **FloatPen**! We are committed to building an open, accessible, and lightweight screen annotation tool for everyone.

We welcome all contributions:
- 🍏 **macOS & 🪟 Windows Ports** (help bring FloatPen to new platforms!)
- 🐛 **Bug fixes** and edge-case testing (X11, Wayland, multi-monitor setups)
- ✨ **New drawing tools** (highlighter enhancements, shapes, callouts)
- 🎨 **UI / Glassmorphic design** polish
- 📦 **Packaging** (Homebrew, Winget, Flatpak, Arch AUR, Snapcraft)
- 📝 **Documentation**, translations, and tutorials

---

## 🧭 Finding Something to Work On

Check out our [GitHub Issues](https://github.com/Khitishnayak/floatpen/issues):
- [`good first issue`](https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) — Great starting points for new contributors.
- [`help wanted`](https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) — Tasks where the community needs hands-on development.
- [`platform:macos`](https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3Aplatform%3Amacos) — macOS Cocoa pass-through and packaging.
- [`platform:windows`](https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3Aplatform%3Awindows) — Windows Win32 pass-through and installer.

Feel free to comment on an issue to say you'd like to work on it, and we'll gladly assign it to you!

---

## 🏗️ Architecture & Multi-Platform Design

FloatPen is designed with a clear separation between the **core annotation engine** and the **platform-specific window layer**:

```
┌────────────────────────────────────────────────────────┐
│               FloatPen Shared Core                     │
│  (Canvas, Toolbar, Vector Models, Undo/Redo, Colors)   │
└──────────────────────────┬─────────────────────────────┘
                           │ calls
                           ▼
┌────────────────────────────────────────────────────────┐
│           Platform Interface (platform_engine.py)       │
│  • enable_click_through(window, boolean)               │
│  • register_global_hotkey(key_combo, callback)        │
└──────────────┬──────────────────┬──────────────────────┘
               │                  │
    ┌──────────▼─────────┐ ┌──────▼──────────┐
    │  macOS Contributor │ │ Win Contributor │
    │  (Cocoa / PyObjC)  │ │ (Win32 ctypes)  │
    └────────────────────┘ └─────────────────┘
```

### 1. Pointer Mode (Click-Through)
The core capability of FloatPen is **Pointer Mode**: drawings stay visible on screen while mouse clicks, dragging, and scrolling pass through directly to background apps.

- **Linux**: Handled via `window.get_window().input_shape_combine_region(cairo.Region(), 0, 0)`.
- **macOS**: Handled via Cocoa `[ns_window setIgnoresMouseEvents:YES]` (using `PyObjC`).
- **Windows**: Handled via Win32 `SetWindowLongPtrW(hwnd, GWL_EXSTYLE, WS_EX_LAYERED | WS_EX_TRANSPARENT)` (using `ctypes`).

### 2. Drawing Engine
Drawing is vector-based (`floatpen/models.py`), rendering smoothed Bézier curves and geometric shapes using Cairo with subpixel precision.

---

## 🛠️ Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Khitishnayak/floatpen.git
cd floatpen
```

### 2. Linux Environment
```bash
# Ubuntu / Debian:
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 libcairo2-dev libx11-dev

# Fedora:
sudo dnf install python3-gobject gtk3 cairo-devel libX11-devel

# Run in development mode:
./run.sh
```

### 3. macOS Environment (WIP)
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install pyobjc-framework-Cocoa pycairo
```

### 4. Windows Environment (WIP)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install pycairo
```

---

## 🧪 Running Unit Tests

Before submitting any code, verify all tests pass:

```bash
python3 -m unittest discover -s tests -v
```

To add new tests, place them under `tests/test_*.py`.

---

## 🚀 Pull Request Workflow

1. **Fork the repo** and create your branch from `main`:
   ```bash
   git checkout -b feat/macos-click-through
   # or
   git checkout -b fix/toolbar-drag-offset
   ```
2. **Follow commit conventions**:
   - `feat(tool): add dashed line drawing mode`
   - `fix(canvas): correct high-DPI scaling on 4K monitors`
   - `docs: update macOS setup instructions`
3. **Verify tests pass**:
   ```bash
   python3 -m unittest discover -s tests -v
   ```
4. **Push to your fork** and submit a Pull Request!
5. Our GitHub Actions CI will automatically test your changes across Python 3.10, 3.11, and 3.12 under headless Xvfb.

---

## 🌟 Contributor Recognition

All contributors will be featured on the README. We believe in recognizing all forms of contribution—code, documentation, bug reports, and design!

Thank you for helping make FloatPen better for everyone! 🖊️✨
