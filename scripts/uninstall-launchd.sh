#!/bin/bash
# Uninstall TMetric Helper LaunchAgent

set -e

PLIST_NAME="com.bukitoka.tmetric-helper.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "=========================================="
echo "TMetric Helper LaunchAgent Uninstaller"
echo "=========================================="

if [ ! -f "$PLIST_DEST" ]; then
    echo "⚠️  LaunchAgent is not installed"
    exit 0
fi

echo "🛑 Stopping and unloading LaunchAgent..."
launchctl unload "$PLIST_DEST" 2>/dev/null || true

echo "🗑️  Removing LaunchAgent configuration..."
rm -f "$PLIST_DEST"

echo ""
echo "=========================================="
echo "✅ Uninstallation complete!"
echo "=========================================="
echo ""
echo "TMetric Helper has been removed from startup."
echo "You can manually delete log files if desired:"
echo "  rm /tmp/tmetric-helper.log"
echo "  rm /tmp/tmetric-helper.error.log"
echo "=========================================="
