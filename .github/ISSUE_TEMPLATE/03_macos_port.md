---
name: "🍏 macOS Port Task"
about: Template for contributors working on native macOS Cocoa support & packaging
title: "[macOS]: "
labels: ["help wanted", "good first issue", "platform:macos", "enhancement"]
---

### 🍏 macOS Support Task

- **Component**: macOS Window Pass-Through & Global Hotkeys
- **Skill Level**: Intermediate Python / macOS Cocoa (`PyObjC` or `ctypes`)
- **Estimated Effort**: 1-2 weekends

#### Objective
Enable click-through pointer mode on macOS:
1. When **Draw Mode** is active: the transparent fullscreen overlay captures clicks and draws.
2. When **Pointer Mode** is active: clicks pass directly through to desktop apps via `[nsWindow setIgnoresMouseEvents:YES]`.

#### Helpful Implementation Notes
- PyObjC `AppKit.NSWindow`:
  ```python
  from AppKit import NSApplication, NSBorderlessWindowMask
  # win.setIgnoresMouseEvents_(True)   # Enable click-through
  # win.setIgnoresMouseEvents_(False)  # Disable click-through (draw mode)
  ```
- Hotkeys on macOS: `pynput.keyboard.GlobalHotKeys` or Cocoa `NSEvent.addGlobalMonitorForEventsMatchingMask_handler_`.
- Release Packaging: `dmgbuild` or `py2app` for generating standalone `.dmg` installer for Apple Silicon and Intel.
