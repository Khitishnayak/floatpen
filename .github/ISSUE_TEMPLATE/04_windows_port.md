---
name: "🪟 Windows Port Task"
about: Template for contributors working on Windows Win32 support & installer
title: "[Windows]: "
labels: ["help wanted", "good first issue", "platform:windows", "enhancement"]
---

### 🪟 Windows Support Task

- **Component**: Win32 Transparent Window & Click-Through
- **Skill Level**: Beginner to Intermediate Python / Win32 API
- **Estimated Effort**: 1-2 weekends

#### Objective
Enable click-through pointer mode on Windows 10/11:
1. When **Draw Mode** is active: overlay captures mouse clicks and draws vector shapes.
2. When **Pointer Mode** is active: clicks pass directly through to background applications via `SetWindowLongPtrW`:
   ```python
   import ctypes
   GWL_EXSTYLE = -20
   WS_EX_LAYERED = 0x00080000
   WS_EX_TRANSPARENT = 0x00000020  # Pass mouse clicks to windows underneath
   ```
3. Register global hotkeys using Win32 `RegisterHotKey` or `keyboard` / `pynput`.

#### Helpful Implementation Notes
- Pure `ctypes` handles Win32 API calls with zero additional pip dependencies.
- Release Packaging: PyInstaller (`pyinstaller --noconsole --onefile ...`) + Inno Setup for standard setup `.exe`.
