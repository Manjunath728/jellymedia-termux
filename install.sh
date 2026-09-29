#!/data/data/com.termux/files/usr/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BIN_DIR="$PREFIX/bin"
SERVICE_DIR="$PREFIX/var/service/jellymedia-mdns"

echo "== JellyMedia Termux Toolkit installer =="

command -v python >/dev/null 2>&1 || pkg install -y python

python -m pip install --upgrade zeroconf

mkdir -p "$BIN_DIR"
cp "$PROJECT_DIR/bin/jellymedia" "$BIN_DIR/jellymedia"
chmod +x "$BIN_DIR/jellymedia"

mkdir -p "$SERVICE_DIR/log" "$HOME/.jellymedia"
cp "$PROJECT_DIR/mdns/jellymedia_mdns.py" "$HOME/.jellymedia/jellymedia_mdns.py"
cp "$PROJECT_DIR/service/jellymedia-mdns/run" "$SERVICE_DIR/run"
cp "$PROJECT_DIR/service/jellymedia-mdns/log/run" "$SERVICE_DIR/log/run"
chmod +x "$SERVICE_DIR/run" "$SERVICE_DIR/log/run"

# Start or restart the mDNS service if termux-services is running
if command -v sv >/dev/null 2>&1; then
    if sv status jellymedia-mdns >/dev/null 2>&1; then
        sv restart jellymedia-mdns >/dev/null 2>&1 || true
    else
        sv up jellymedia-mdns >/dev/null 2>&1 || true
    fi
fi

echo
echo "Installed:"
echo "  $BIN_DIR/jellymedia"
echo "  $SERVICE_DIR"
echo
echo "Run:"
echo "  jellymedia status"
echo "  jellymedia organize"
echo
echo "mDNS service:"
echo "  sv up jellymedia-mdns"
echo "  sv status jellymedia-mdns"
