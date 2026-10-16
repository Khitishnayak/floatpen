#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo "=== Installing FloatPen ==="

# 1. Install CLI wrapper to ~/.local/bin
mkdir -p "$HOME/.local/bin"
ln -sf "$DIR/run.sh" "$HOME/.local/bin/floatpen"
chmod +x "$HOME/.local/bin/floatpen"
echo "✓ Installed executable to $HOME/.local/bin/floatpen"

# 2. Install icon
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$ICON_DIR"
cp "$DIR/assets/floatpen.png" "$ICON_DIR/floatpen.png"
echo "✓ Installed icon to $ICON_DIR/floatpen.png"

# 3. Install desktop launcher
APP_DIR="$HOME/.local/share/applications"
mkdir -p "$APP_DIR"
cat << EOF > "$APP_DIR/floatpen.desktop"
[Desktop Entry]
Name=FloatPen
Comment=Floating desktop marker and screen annotation tool like Epic Pen
Exec=$HOME/.local/bin/floatpen
Icon=$ICON_DIR/floatpen.png
Terminal=false
Type=Application
Categories=Utility;Graphics;
Keywords=screen;marker;draw;pen;epic;annotation;presentation;whiteboard;floating;
StartupNotify=true
EOF
chmod +x "$APP_DIR/floatpen.desktop"
echo "✓ Installed desktop entry to $APP_DIR/floatpen.desktop"

# 4. Update desktop database if available
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APP_DIR" || true
fi

echo "=== Installation Complete! ==="
echo "You can launch FloatPen by typing: floatpen"
echo "Or searching for 'FloatPen' in your application launcher."
