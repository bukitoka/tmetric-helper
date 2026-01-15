#!/bin/bash
# Run TMetric Helper in the background without installing as LaunchAgent
# Useful for testing or temporary background execution

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_DIR/tmetric-helper.log"

echo "Starting TMetric Helper in background..."
echo "Log file: $LOG_FILE"

cd "$PROJECT_DIR"

# Kill any existing background processes
pkill -f "tmetric-helper auto-keep-active" 2>/dev/null || true

# Run in background with nohup
nohup "$PROJECT_DIR/dist/tmetric-helper" auto-keep-active --inactivity-timeout 300 --check-interval 10 > "$LOG_FILE" 2>&1 &

PID=$!
echo "✅ Started with PID: $PID"
echo ""
echo "Useful commands:"
echo "  View logs:      tail -f $LOG_FILE"
echo "  Check status:   ps aux | grep tmetric-helper"
echo "  Stop:           pkill -f 'tmetric-helper auto-keep-active'"
echo ""
