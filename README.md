# FloatPen 🖊️

<p align="center">
  <img src="assets/floatpen.png" width="128" height="128" alt="FloatPen Logo" />
</p>

<p align="center">
  <strong>A lightweight, responsive floating desktop marker and screen annotation tool for Linux inspired by Epic Pen.</strong>
</p>

<p align="center">
  <a href="https://github.com/Khitishnayak/floatpen/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-brightgreen.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Linux%20(X11%20%2F%20Wayland)-orange.svg" alt="Platform: Linux">
  <a href="https://github.com/Khitishnayak/floatpen/actions/workflows/ci.yml"><img src="https://github.com/Khitishnayak/floatpen/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
</p>

---

**FloatPen** lets you draw, highlight, place arrows & shapes, and write text notes directly over any live application, desktop, video player, slide deck, or browser with instant click-through toggling.

---

## ✨ Features

- **🖱️ Pointer Mode (Click-Through)**:
  - Annotations remain visible on top of your screen, while all mouse clicks, drags, and scrolling pass directly through to whatever desktop application or browser is underneath!
  - Toggle instantly using the floating toolbar button, <kbd>Alt + D</kbd>, or <kbd>Ctrl + Shift + A</kbd>.
- **✏️ Draw Mode**:
  - Fullscreen transparent overlay captures drawing input with subpixel vector rendering.
- **🖊️ Comprehensive Drawing Suite**:
  - **Pen (`P`)**: Freehand smooth vector drawing with midpoint Bezier curve smoothing.
  - **Highlighter (`H`)**: Wide semi-transparent marker stroke (35% opacity) that highlights without obscuring underlying text or diagrams.
  - **Eraser (`E`)**: Intelligent stroke-based eraser that cleanly removes intersected items in a single click or drag.
  - **Arrow (`A`)**: Directional arrow with a crisp, aerodynamic arrowhead (essential for tutorials and presentations).
  - **Line (`L`)**: Straight line tool with 15° angle snap when holding <kbd>Shift</kbd>.
  - **Rectangle (`R`)**: Clean rounded box tool with 1:1 square snap when holding <kbd>Shift</kbd>.
  - **Circle / Ellipse (`C`)**: Smooth ellipse tool with circle snap when holding <kbd>Shift</kbd>.
  - **Text (`T`)**: Click anywhere to type custom text annotations with anti-aliasing via PangoCairo.
- **🎨 Color Palette & Stroke Sizes**:
  - 8 curated modern colors: Red, Orange, Yellow, Green, Blue, Purple, White, Charcoal/Black.
  - Custom color picker dialog (`+ custom`) to select any hex color.
  - 4 stroke thickness levels: Fine (3px), Medium (6px), Thick (12px), Extra Bold (20px).
- **📋 Board Modes**:
  - **Desktop (Transparent)**: Draw directly over the live desktop.
  - **Whiteboard (`W`)**: Solid crisp white digital whiteboard.
  - **Blackboard (`B`)**: Solid dark chalkboard background.
  - Cycle through them using the Board button.
- **⚡ Actions & History**:
  - **Undo (`Ctrl+Z`)** & **Redo (`Ctrl+Y`)**
  - **Hide / Show Ink (Eye icon)**: Temporarily hide annotations to inspect the clean screen below, then restore them with a single click.
  - **Clear All (`Ctrl+K`)**: Clears screen with undo capability.
  - **Screenshot / Save (`Ctrl+S`)**: Saves current annotations/board to `~/Pictures/Screenshots/floatpen_<timestamp>.png` and automatically copies the image to the system clipboard.
- **🪟 Floating Draggable & Collapsible Toolbar**:
  - Modern glassmorphic dark theme (`#18181b` with subtle borders and shadows).
  - Drag handle to position the palette anywhere on your screens.
  - Minimize button (<kbd>▲</kbd>/<kbd>▼</kbd>) folds the toolbar into a tiny 44px capsule when not actively changing tools.

---

## 🚀 Installation & Setup

### Option 1: Ubuntu / Debian Package (.deb)

Download and install the official package directly from [Releases](https://github.com/Khitishnayak/floatpen/releases/latest):

```bash
# Download latest deb package
wget https://github.com/Khitishnayak/floatpen/releases/latest/download/floatpen_1.0.0_all.deb

# Install
sudo apt install ./floatpen_1.0.0_all.deb
```
Or simply double-click the `.deb` file in your file manager to install through the **Ubuntu App Center**.

### Option 2: Quick Install from Source (Git)

```bash
git clone https://github.com/Khitishnayak/floatpen.git
cd floatpen
./install.sh
```

### Option 3: Pip / Pipx Install

```bash
pip install git+https://github.com/Khitishnayak/floatpen.git
```

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut | Scope |
|---|---|---|
| **Toggle Draw / Pointer Mode** | <kbd>Alt + D</kbd> or <kbd>Ctrl + Shift + A</kbd> or <kbd>F8</kbd> | **Global** |
| **Exit to Pointer Mode** | <kbd>Esc</kbd> or Right-Click | In-App |
| **Activate Pen** | <kbd>P</kbd> | In-App |
| **Activate Highlighter** | <kbd>H</kbd> | In-App |
| **Activate Eraser** | <kbd>E</kbd> | In-App |
| **Activate Arrow** | <kbd>A</kbd> | In-App |
| **Activate Line** | <kbd>L</kbd> | In-App |
| **Activate Rectangle** | <kbd>R</kbd> | In-App |
| **Activate Circle** | <kbd>C</kbd> | In-App |
| **Activate Text** | <kbd>T</kbd> | In-App |
| **Whiteboard Mode** | <kbd>W</kbd> | In-App |
| **Blackboard Mode** | <kbd>B</kbd> | In-App |
| **Undo** | <kbd>Ctrl + Z</kbd> | In-App |
| **Redo** | <kbd>Ctrl + Y</kbd> | In-App |
| **Clear All** | <kbd>Ctrl + K</kbd> | In-App |
| **Save & Copy Screenshot** | <kbd>Ctrl + S</kbd> | In-App |
| **Angle / Square Snap** | Hold <kbd>Shift</kbd> while dragging | In-App |

---

## 🛠️ Tech Stack & Architecture

- **Python 3** with standard libraries.
- **GTK 3.24 (PyGObject)** & **Cairo** for hardware-accelerated 2D vector drawing.
- **PangoCairo** for crisp subpixel typography.
- **X11 / XWayland transparent overlay** with `input_shape_combine_region` for instantaneous click-through switching.
- **libX11 ctypes daemon** for global hotkey grabbing across all workspaces.
- **Zero heavy dependencies**: Starts in < 0.2s with ~35MB RAM consumption.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on setting up your development environment, reporting bugs, and submitting pull requests.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
