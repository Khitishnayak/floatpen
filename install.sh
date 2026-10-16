#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo "=== Installing EpicMarker ==="

# 1. Install CLI wrapper to ~/.local/bin
mkdir -p "$HOME/.local/bin"
ln -sf "$DIR/run.sh" "$HOME/.local/bin/epicmarker"
chmod +x "$HOME/.local/bin/epicmarker"
echo "✓ Installed executable to $HOME/.local/bin/epicmarker"

# 2. Install icon
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$ICON_DIR"
cp "$DIR/assets/epicmarker.png" "$ICON_DIR/epicmarker.png"
echo "✓ Installed icon to $ICON_DIR/epicmarker.png"

# 3. Install desktop launcher
APP_DIR="$HOME/.local/share/applications"
mkdir -p "$APP_DIR"
cat << EOF > "$APP_DIR/epicmarker.desktop"
[Desktop Entry]
Name=EpicMarker
Comment=Desktop marker and screen annotation tool like Epic Pen
Exec=$HOME/.local/bin/epicmarker
Icon=$ICON_DIR/epicmarker.png
Terminal=false
Type=Application
Categories=Utility;Graphics;
Keywords=screen;marker;draw;pen;epic;annotation;presentation;whiteboard;
StartupNotify=true
EOF
chmod +x "$APP_DIR/epicmarker.desktop"
echo "✓ Installed desktop entry to $APP_DIR/epicmarker.desktop"

# 4. Update desktop database if available
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APP_DIR" || true
fi

echo "=== Installation Complete! ==="
echo "You can launch EpicMarker by typing: epicmarker"
echo "Or searching for 'EpicMarker' in your application launcher."
