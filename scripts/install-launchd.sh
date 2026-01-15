#!/bin/bash
# Install TMetric Helper as a macOS LaunchAgent
# This will make it run automatically on login and in the background

set -e

PLIST_NAME="com.bukitoka.tmetric-helper.plist"
PLIST_SOURCE="$(cd "$(dirname "$0")/.." && pwd)/launchd/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
EXECUTABLE="$(cd "$(dirname "$0")/.." && pwd)/dist/tmetric-helper"

echo "=========================================="
echo "TMetric Helper LaunchAgent Installer"
echo "=========================================="

# Check if executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "❌ Error: Executable not found at $EXECUTABLE"
    echo "Please build the project first: uv run python build.py"
    exit 1
fi

# Check if plist source exists
if [ ! -f "$PLIST_SOURCE" ]; then
    echo "❌ Error: LaunchAgent plist not found at $PLIST_SOURCE"
    exit 1
fi

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$HOME/Library/LaunchAgents"

# Update the plist with the correct executable path
echo "📝 Creating LaunchAgent configuration..."
sed "s|/Volumes/Devs/tmetric-helper/dist/tmetric-helper|$EXECUTABLE|g" "$PLIST_SOURCE" > "$PLIST_DEST"

# Unload if already loaded (ignore errors)
launchctl unload "$PLIST_DEST" 2>/dev/null || true

# Load the LaunchAgent
echo "🚀 Loading LaunchAgent..."
launchctl load "$PLIST_DEST"

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "TMetric Helper is now running in the background and will:"
echo "  • Start automatically on login"
echo "  • Monitor for TMetric process every 30 seconds"
echo "  • Move mouse automatically after 5 minutes of inactivity (only when TMetric is running)"
echo "  • Restart automatically if it crashes"
echo ""
echo "Logs are available at:"
echo "  Output: /tmp/tmetric-helper.log"
echo "  Errors: /tmp/tmetric-helper.error.log"
echo ""
echo "Useful commands:"
echo "  View status:    launchctl list | grep tmetric-helper"
echo "  View logs:      tail -f /tmp/tmetric-helper.log"
echo "  Restart:        launchctl kickstart -k gui/\$(id -u)/$PLIST_NAME"
echo "  Uninstall:      ./scripts/uninstall-launchd.sh"
echo "=========================================="
