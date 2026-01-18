#!/bin/bash

# TMetric Helper - LaunchD Service Management Script
# This script helps install, uninstall, and manage the launchd service

set -e

PLIST_NAME="com.bukitoka.tmetric-helper.plist"
PLIST_SOURCE="$(cd "$(dirname "$0")" && pwd)/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
SERVICE_NAME="com.bukitoka.tmetric-helper"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_plist_exists() {
    if [ ! -f "$PLIST_SOURCE" ]; then
        print_error "Plist file not found: $PLIST_SOURCE"
        exit 1
    fi
}

install_service() {
    print_header "Installing TMetric Helper LaunchD Service"

    check_plist_exists

    # Create LaunchAgents directory if it doesn't exist
    mkdir -p "$HOME/Library/LaunchAgents"

    # Copy plist file
    print_info "Copying plist file..."
    cp "$PLIST_SOURCE" "$PLIST_DEST"
    print_success "Plist copied to $PLIST_DEST"

    # Load the service
    print_info "Loading service..."
    launchctl load "$PLIST_DEST"
    print_success "Service loaded"

    echo ""
    print_success "Installation complete!"
    print_info "The service will:"
    echo "  • Check every 30 minutes if it should be running"
    echo "  • Only run during work hours (Mon-Fri, 9 AM - 6 PM)"
    echo "  • Exit immediately if outside work hours"
    echo "  • Automatically restart if it crashes during work hours"
    echo ""
    print_info "Check status with: $0 status"
    print_info "View logs with: $0 logs"
}

uninstall_service() {
    print_header "Uninstalling TMetric Helper LaunchD Service"

    if [ ! -f "$PLIST_DEST" ]; then
        print_warning "Service is not installed"
        exit 0
    fi

    # Unload the service
    print_info "Unloading service..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
    print_success "Service unloaded"

    # Remove plist file
    print_info "Removing plist file..."
    rm "$PLIST_DEST"
    print_success "Plist removed"

    echo ""
    print_success "Uninstallation complete!"
}

restart_service() {
    print_header "Restarting TMetric Helper LaunchD Service"

    if [ ! -f "$PLIST_DEST" ]; then
        print_error "Service is not installed. Install it first with: $0 install"
        exit 1
    fi

    print_info "Unloading service..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
    print_success "Service unloaded"

    print_info "Loading service..."
    launchctl load "$PLIST_DEST"
    print_success "Service loaded"

    echo ""
    print_success "Service restarted!"
}

status_service() {
    print_header "TMetric Helper LaunchD Service Status"

    if [ ! -f "$PLIST_DEST" ]; then
        print_warning "Service is not installed"
        echo ""
        print_info "Install with: $0 install"
        exit 0
    fi

    print_success "Service is installed at: $PLIST_DEST"
    echo ""

    # Check if service is loaded
    if launchctl list | grep -q "$SERVICE_NAME"; then
        print_success "Service is loaded"
        echo ""
        launchctl list | grep "$SERVICE_NAME" || true
    else
        print_warning "Service is not loaded"
        echo ""
        print_info "Load it with: $0 restart"
    fi
}

view_logs() {
    print_header "TMetric Helper Logs"

    STDOUT_LOG="/tmp/tmetric-helper.log"
    STDERR_LOG="/tmp/tmetric-helper.error.log"

    if [ -f "$STDOUT_LOG" ]; then
        print_info "Standard Output Log:"
        echo "----------------------------------------"
        tail -n 50 "$STDOUT_LOG"
        echo ""
    else
        print_warning "No standard output log found at $STDOUT_LOG"
    fi

    if [ -f "$STDERR_LOG" ]; then
        print_info "Standard Error Log:"
        echo "----------------------------------------"
        tail -n 50 "$STDERR_LOG"
        echo ""
    else
        print_info "No error log found (this is good!)"
    fi

    echo ""
    print_info "To follow logs in real-time:"
    echo "  tail -f $STDOUT_LOG"
    echo "  tail -f $STDERR_LOG"
}

clear_logs() {
    print_header "Clearing TMetric Helper Logs"

    STDOUT_LOG="/tmp/tmetric-helper.log"
    STDERR_LOG="/tmp/tmetric-helper.error.log"

    if [ -f "$STDOUT_LOG" ]; then
        > "$STDOUT_LOG"
        print_success "Cleared stdout log"
    fi

    if [ -f "$STDERR_LOG" ]; then
        > "$STDERR_LOG"
        print_success "Cleared stderr log"
    fi

    print_success "Logs cleared"
}

show_help() {
    print_header "TMetric Helper LaunchD Service Manager"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install     Install and start the service"
    echo "  uninstall   Stop and remove the service"
    echo "  restart     Restart the service"
    echo "  status      Show service status"
    echo "  logs        View recent logs"
    echo "  clear-logs  Clear log files"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install       # Install the service"
    echo "  $0 status        # Check if service is running"
    echo "  $0 logs          # View recent logs"
    echo "  $0 restart       # Restart after updating code"
    echo ""
    echo "Service Configuration:"
    echo "  • Runs: Monday-Friday, 9 AM - 6 PM"
    echo "  • Checks every: 30 minutes"
    echo "  • Inactivity timeout: 5 minutes"
    echo "  • Logs: /tmp/tmetric-helper.log"
    echo ""
}

# Main script logic
case "${1:-help}" in
    install)
        install_service
        ;;
    uninstall)
        uninstall_service
        ;;
    restart)
        restart_service
        ;;
    status)
        status_service
        ;;
    logs)
        view_logs
        ;;
    clear-logs)
        clear_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
