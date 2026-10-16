#!/usr/bin/env bash
DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" >/dev/null 2>&1 && pwd)"
export PYTHONPATH="$DIR:$PYTHONPATH"
if [ -n "$WAYLAND_DISPLAY" ] && [ -z "$GDK_BACKEND" ]; then
    export GDK_BACKEND=x11
fi
exec python3 "$DIR/floatpen/main.py" "$@"
