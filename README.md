# FloatPen 🖊️

<p align="center">
  <img src="assets/floatpen.png" width="128" height="128" alt="FloatPen Logo" />
</p>

<p align="center">
  <strong>An open-source, lightweight, cross-platform floating desktop marker and screen annotation tool for Linux, Windows, and macOS inspired by Epic Pen.</strong>
</p>

<p align="center">
  <a href="https://github.com/Khitishnayak/floatpen/releases/latest"><img src="https://img.shields.io/github/v/release/Khitishnayak/floatpen?color=blue&label=Latest%20Release" alt="Release"></a>
  <a href="https://github.com/Khitishnayak/floatpen/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-brightgreen.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platforms-Linux%20%7C%20Windows%20%7C%20macOS-orange.svg" alt="Platforms">
  <a href="https://github.com/Khitishnayak/floatpen/actions/workflows/ci.yml"><img src="https://github.com/Khitishnayak/floatpen/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <a href="https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22"><img src="https://img.shields.io/github/issues/Khitishnayak/floatpen/good%20first%20issue?color=7057ff&label=Good%20First%20Issues" alt="Good First Issues"></a>
  <a href="https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22"><img src="https://img.shields.io/github/issues/Khitishnayak/floatpen/help%20wanted?color=008672&label=Help%20Wanted" alt="Help Wanted"></a>
  <a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

---

**FloatPen** allows you to draw, highlight, place arrows & shapes, and write text notes directly over any live application, desktop, video player, slide deck, or browser with instant click-through toggling.

---

## 📥 Direct Downloads

Download pre-packaged releases directly from [GitHub Releases](https://github.com/Khitishnayak/floatpen/releases/latest):

| Operating System | Download Link | Quick Instructions |
|---|---|---|
| **🐧 Linux (Debian / Ubuntu)** | [**`floatpen_1.0.0_all.deb`**](https://github.com/Khitishnayak/floatpen/releases/download/v1.0.1/floatpen_1.0.0_all.deb) | Double-click or `sudo apt install ./floatpen_1.0.0_all.deb` |
| **🪟 Windows (10 / 11)** | [**`floatpen-1.0.0-windows-portable.zip`**](https://github.com/Khitishnayak/floatpen/releases/download/v1.0.1/floatpen-1.0.0-windows-portable.zip) | Extract zip and double-click `FloatPen.bat` |
| **🍏 macOS (Apple & Intel)** | [**`floatpen-1.0.0-macos-portable.zip`**](https://github.com/Khitishnayak/floatpen/releases/download/v1.0.1/floatpen-1.0.0-macos-portable.zip) | Extract zip and double-click `FloatPen.command` |
| **🐍 Python Wheel (Universal)** | [**`floatpen-1.0.0-py3-none-any.whl`**](https://github.com/Khitishnayak/floatpen/releases/download/v1.0.1/floatpen-1.0.0-py3-none-any.whl) | `pip install floatpen-1.0.0-py3-none-any.whl` |
| **📦 Source Tarball** | [**`floatpen-1.0.0.tar.gz`**](https://github.com/Khitishnayak/floatpen/releases/download/v1.0.1/floatpen-1.0.0.tar.gz) | `tar -xvf floatpen-1.0.0.tar.gz` |

---

## ✨ Features

- **🖱️ Pointer Mode (Click-Through Pass-Through)**:
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

## 🚀 Installation & Setup by Platform

### 🐧 Linux (Ubuntu, Debian, Fedora, Arch)

#### Option 1: Debian / Ubuntu Package (.deb)
```bash
wget https://github.com/Khitishnayak/floatpen/releases/latest/download/floatpen_1.0.0_all.deb
sudo apt install ./floatpen_1.0.0_all.deb
floatpen
```

#### Option 2: Install from Source
```bash
git clone https://github.com/Khitishnayak/floatpen.git
cd floatpen
./install.sh
floatpen
```

---

### 🪟 Windows (10 & 11)

#### Option 1: Portable Zip
1. Download [**`floatpen-1.0.0-windows-portable.zip`**](https://github.com/Khitishnayak/floatpen/releases/download/v1.0.1/floatpen-1.0.0-windows-portable.zip).
2. Extract the folder anywhere on your computer.
3. Double-click **`FloatPen.bat`** to start annotating!
4. (Optional) Run `install.ps1` in PowerShell to generate a Desktop shortcut.

#### Option 2: Pip / Pipx
```powershell
pip install git+https://github.com/Khitishnayak/floatpen.git
python -m floatpen.main
```

---

### 🍏 macOS (Apple Silicon M1/M2/M3 & Intel)

#### Option 1: Portable Zip
1. Download [**`floatpen-1.0.0-macos-portable.zip`**](https://github.com/Khitishnayak/floatpen/releases/download/v1.0.1/floatpen-1.0.0-macos-portable.zip).
2. Extract the archive in your Downloads or Applications folder.
3. Double-click **`FloatPen.command`** in Finder to launch!

#### Option 2: Terminal / Homebrew
```bash
git clone https://github.com/Khitishnayak/floatpen.git
cd floatpen
./run.sh
```

---

## ⌨️ Keyboard Shortcuts

| Action | Linux / Windows | macOS | Scope |
|---|---|---|---|
| **Toggle Draw / Pointer Mode** | <kbd>Alt + D</kbd> or <kbd>Ctrl + Shift + A</kbd> | <kbd>⌥ + D</kbd> or <kbd>⌘ + ⇧ + A</kbd> | **Global** |
| **Exit to Pointer Mode** | <kbd>Esc</kbd> or Right-Click | <kbd>Esc</kbd> or Right-Click | In-App |
| **Activate Pen** | <kbd>P</kbd> | <kbd>P</kbd> | In-App |
| **Activate Highlighter** | <kbd>H</kbd> | <kbd>H</kbd> | In-App |
| **Activate Eraser** | <kbd>E</kbd> | <kbd>E</kbd> | In-App |
| **Activate Arrow** | <kbd>A</kbd> | <kbd>A</kbd> | In-App |
| **Activate Line** | <kbd>L</kbd> | <kbd>L</kbd> | In-App |
| **Activate Rectangle** | <kbd>R</kbd> | <kbd>R</kbd> | In-App |
| **Activate Circle** | <kbd>C</kbd> | <kbd>C</kbd> | In-App |
| **Activate Text** | <kbd>T</kbd> | <kbd>T</kbd> | In-App |
| **Whiteboard Mode** | <kbd>W</kbd> | <kbd>W</kbd> | In-App |
| **Blackboard Mode** | <kbd>B</kbd> | <kbd>B</kbd> | In-App |
| **Undo** | <kbd>Ctrl + Z</kbd> | <kbd>⌘ + Z</kbd> | In-App |
| **Redo** | <kbd>Ctrl + Y</kbd> | <kbd>⌘ + Y</kbd> | In-App |
| **Clear All** | <kbd>Ctrl + K</kbd> | <kbd>⌘ + K</kbd> | In-App |
| **Save & Copy Screenshot** | <kbd>Ctrl + S</kbd> | <kbd>⌘ + S</kbd> | In-App |
| **Angle / Square Snap** | Hold <kbd>Shift</kbd> while dragging | Hold <kbd>Shift</kbd> while dragging | In-App |

---

## 🗺️ Multi-Platform Roadmap & Contributing

FloatPen is an active open-source project and welcomes community contributors!

| Platform | Engine Backend | Click-Through API | Status | Contributor Task |
|---|---|---|---|---|
| **🐧 Linux** | GTK 3 / Cairo | `gdk_window_input_shape_combine_region` | **Live (v1.0.1)** | Feature additions & Wayland testing |
| **🍏 macOS** | Cocoa / PyObjC | `[nsWindow setIgnoresMouseEvents:YES]` | **Available in v1.0.1** | [Contribute Cocoa Hook #1](https://github.com/Khitishnayak/floatpen/issues/1) |
| **🪟 Windows** | Win32 / ctypes | `WS_EX_LAYERED \| WS_EX_TRANSPARENT` | **Available in v1.0.1** | [Contribute Win32 Hook #2](https://github.com/Khitishnayak/floatpen/issues/2) |
| **📦 Packaging** | Homebrew / Winget / Flatpak | CLI / App Store manifests | **Help Wanted** | [Contribute Package Formula #3](https://github.com/Khitishnayak/floatpen/issues/3) |

Looking for a place to start? Pick any issue tagged [`good first issue`](https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) or [`help wanted`](https://github.com/Khitishnayak/floatpen/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) and check our [CONTRIBUTING.md](CONTRIBUTING.md) guide!

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on setting up your development environment, reporting bugs, and submitting pull requests.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
