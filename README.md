# TMetric Helper

A Python CLI tool for automating mouse movements and keyboard typing on macOS, with automatic work hours protection.

## Features

- **Mouse Movement**: Move the mouse pointer to specific coordinates
- **Automatic Typing**: Type text automatically with configurable intervals
- **Click Automation**: Click at specific coordinates or current position
- **Key Pressing**: Press keyboard keys programmatically
- **Position Detection**: Get current mouse position
- **Command Sequences**: Execute multiple commands in sequence
- **Keep System Active**: Prevent system sleep/inactivity with automatic mouse movements
- **Process Monitoring**: Watch for TMetric Desktop and perform actions only when it's running
- **Work Hours Protection**: Automatically refuses to run outside business hours (Mon-Fri, 9 AM - 6 PM)
- **Background Service**: Run as a macOS LaunchAgent with automatic startup

## Quick Start

```bash
# Install dependencies
uv sync

# Install as background service (recommended)
cd launchd
./install.sh install

# Check status
./install.sh status

# View logs
./install.sh logs
```

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync
```

### Building Standalone Executable (Optional)

You can build a standalone executable binary:

```bash
# Build the executable
uv run python build.py

# The executable will be created in the dist/ directory
./dist/tmetric-helper --help
```

**Note**: The LaunchAgent service uses `uv run` directly, so building the executable is optional unless you need a standalone binary.

## Usage

### Basic Commands

**Get current mouse position:**
```bash
uv run tmetric-helper position
```

**Move mouse to coordinates:**
```bash
uv run tmetric-helper move 100 200
uv run tmetric-helper move 100 200 --duration 2.0
```

**Type text automatically:**
```bash
uv run tmetric-helper type-text "Hello, World!"
uv run tmetric-helper type-text "Hello" --interval 0.2 --delay 3
```

**Click at coordinates:**
```bash
uv run tmetric-helper click-at --x 100 --y 200
uv run tmetric-helper click-at --x 100 --y 200 --clicks 2 --button right
```

**Press a key:**
```bash
uv run tmetric-helper press enter
uv run tmetric-helper press space --presses 3
```

### Keep System Active

**Monitor for inactivity and perform actions automatically:**
```bash
# Default: Move mouse after 5 minutes of inactivity
uv run tmetric-helper keep-active

# Custom timeout (e.g., 3 minutes = 180 seconds)
uv run tmetric-helper keep-active --inactivity-timeout 180

# Different actions
uv run tmetric-helper keep-active --action jiggle  # Wiggle mouse in circle
uv run tmetric-helper keep-active --action press   # Press shift key

# Custom check interval (check every 30 seconds)
uv run tmetric-helper keep-active --check-interval 30
```

The `keep-active` command runs continuously and monitors both mouse and keyboard activity. When no activity is detected for the specified timeout period (default: 5 minutes), it performs a subtle action to keep the system active. Press Ctrl+C to stop monitoring.

### Process Monitoring

**Check if TMetric is running:**
```bash
# Check once
uv run tmetric-helper is-running

# Check for a different process
uv run tmetric-helper is-running --process-name "Visual Studio Code"
```

**Monitor for TMetric and notify when it's running:**
```bash
# Continuously monitor (checks every 5 seconds)
uv run tmetric-helper watch

# Check once and exit
uv run tmetric-helper watch --run-once

# Custom check interval (every 10 seconds)
uv run tmetric-helper watch --check-interval 10
```

**Automatically keep system active when TMetric is running:**
```bash
# Default: Move mouse after 5 minutes of inactivity (only when TMetric is running)
uv run tmetric-helper auto-keep-active

# Custom inactivity timeout (3 minutes)
uv run tmetric-helper auto-keep-active --inactivity-timeout 180

# Different action types
uv run tmetric-helper auto-keep-active --action jiggle  # Wiggle mouse
uv run tmetric-helper auto-keep-active --action press   # Press shift key

# Custom intervals
uv run tmetric-helper auto-keep-active --check-interval 15 --process-check-interval 60
```

The `auto-keep-active` command combines process monitoring with activity simulation. It only performs mouse movements when TMetric is detected running AND no user activity is detected for the specified timeout period.

### Advanced: Command Sequences

Execute multiple commands in sequence:

```bash
uv run tmetric-helper sequence "move:100,200" "click" "type:hello" "press:enter"
```

Available sequence commands:
- `move:x,y` - Move mouse to coordinates
- `click` - Click at current position
- `type:text` - Type text
- `press:key` - Press a key
- `wait:seconds` - Wait for specified seconds

## Work Hours Protection

All commands include a work hours check at startup that prevents them from running outside of business hours:

- **Work Hours:** Monday-Friday, 9:00 AM - 6:00 PM
- **Weekend:** Commands exit gracefully on Saturday and Sunday
- **After Hours:** Commands exit gracefully before 9:00 AM or after 6:00 PM on weekdays

**Example output when run outside work hours:**
```
============================================================
⏸️  Outside Work Hours
============================================================
Today: Saturday
Current time: 11:00 AM

Work hours: Monday-Friday, 9:00 AM - 6:00 PM

📅 It's the weekend! Time to relax.

Exiting gracefully...
============================================================
```

This ensures that automation only runs during typical business hours, preventing unnecessary activity tracking during personal time.

### Customizing Work Hours

To change work hours, edit `src/tmetric_helper/cli.py`, function `is_work_hours()`:

```python
def is_work_hours():
    """Check if current time is within work hours."""
    now = datetime.now()
    is_weekday = now.weekday() < 5  # 0-4 are Monday-Friday
    is_work_time = 9 <= now.hour < 18  # 9 AM to 6 PM
    return is_weekday and is_work_time
```

**Examples:**
- **7 AM - 5 PM**: Change to `7 <= now.hour < 17`
- **Include Saturday**: Change to `now.weekday() < 6`
- **24/7 mode**: Return `True` (not recommended)

After changes, restart the service:
```bash
cd launchd
./install.sh restart
```

## Running as Background Service (LaunchAgent)

The recommended way to run TMetric Helper is as a macOS LaunchAgent, which runs automatically in the background.

### Installation

```bash
cd launchd
./install.sh install
```

This will:
- Copy the service configuration to `~/Library/LaunchAgents/`
- Load the service with launchd
- Start monitoring automatically

### Service Management

The `install.sh` script provides complete service management:

```bash
# Install and start the service
./install.sh install

# Check service status
./install.sh status

# View recent logs
./install.sh logs

# Restart service (after code changes)
./install.sh restart

# Uninstall service
./install.sh uninstall

# Clear log files
./install.sh clear-logs
```

### What the Service Does

When installed, the LaunchAgent:

1. ✅ **Starts automatically** when you log in
2. ✅ **Runs in background** (no terminal window)
3. ✅ **Checks every 30 minutes** if it should be running
4. ✅ **Only runs during work hours** (Mon-Fri, 9 AM - 6 PM)
5. ✅ **Exits immediately** if outside work hours
6. ✅ **Monitors for TMetric Desktop** every 30 seconds
7. ✅ **Moves mouse** after 5 minutes of inactivity (only when TMetric is running)
8. ✅ **Auto-restarts** if it crashes during work hours
9. ✅ **Doesn't restart** on normal exit (outside work hours)

### Service Behavior

#### During Work Hours (Mon-Fri, 9 AM - 6 PM)
```
[09:00:15] ✓ TMetric Desktop is running - monitoring active
[09:00:25] Active - Idle: 10s - Mouse: (1024, 768) - Timeout in 290s
[09:05:25] ⚠️  INACTIVE for 300s - Performing move...
[09:05:25] ✓ Action completed (total: 1)
```

The service runs continuously, monitoring for TMetric and performing keep-alive actions.

#### Outside Work Hours (Weekends or Before/After Hours)
```
============================================================
⏸️  Outside Work Hours
============================================================
Today: Saturday
Current time: 11:30 AM

Work hours: Monday-Friday, 9:00 AM - 6:00 PM

📅 It's the weekend! Time to relax.

Exiting gracefully...
============================================================
```

The service:
1. Tries to start every 30 minutes (configured with `StartInterval`)
2. Checks work hours at startup
3. Exits gracefully (exit code 0) if outside work hours
4. LaunchD does NOT restart it (due to `SuccessfulExit: false`)
5. Will try again in 30 minutes automatically

This ensures the service automatically resumes when work hours begin.

### Logs

Logs are written to:
- **Standard Output**: `/tmp/tmetric-helper.log`
- **Standard Error**: `/tmp/tmetric-helper.error.log`

**View logs:**
```bash
# Using the install script
cd launchd
./install.sh logs

# Or directly
tail -f /tmp/tmetric-helper.log
tail -f /tmp/tmetric-helper.error.log
```

**Clear logs:**
```bash
cd launchd
./install.sh clear-logs
```

### Service Configuration

The service is configured in `launchd/com.bukitoka.tmetric-helper.plist`:

**Default settings:**
- **Command**: `uv run tmetric-helper auto-keep-active`
- **Inactivity Timeout**: 300 seconds (5 minutes)
- **Activity Check Interval**: 10 seconds
- **Process Check Interval**: 30 seconds
- **Service Start Interval**: 1800 seconds (30 minutes)
- **Throttle Interval**: 60 seconds

**To customize**, edit the plist file and change the `ProgramArguments`:

```xml
<key>ProgramArguments</key>
<array>
    <string>/opt/homebrew/bin/uv</string>
    <string>run</string>
    <string>tmetric-helper</string>
    <string>auto-keep-active</string>
    <string>--inactivity-timeout</string>
    <string>600</string>  <!-- 10 minutes instead of 5 -->
    <string>--check-interval</string>
    <string>30</string>   <!-- Check every 30 seconds -->
</array>
```

After changes, restart the service:
```bash
cd launchd
./install.sh restart
```

### Manual Service Control

You can also control the service using `launchctl` directly:

```bash
# Check if service is loaded
launchctl list | grep tmetric-helper

# Load service
launchctl load ~/Library/LaunchAgents/com.bukitoka.tmetric-helper.plist

# Unload service
launchctl unload ~/Library/LaunchAgents/com.bukitoka.tmetric-helper.plist

# Force start service now
launchctl start com.bukitoka.tmetric-helper

# Force stop service now
launchctl stop com.bukitoka.tmetric-helper

# Restart service
launchctl kickstart -k gui/$(id -u)/com.bukitoka.tmetric-helper
```

## Troubleshooting

### Service Won't Start

1. **Check if the plist file exists:**
   ```bash
   ls -l ~/Library/LaunchAgents/com.bukitoka.tmetric-helper.plist
   ```

2. **Validate the plist syntax:**
   ```bash
   plutil ~/Library/LaunchAgents/com.bukitoka.tmetric-helper.plist
   ```

3. **Check the error log:**
   ```bash
   cat /tmp/tmetric-helper.error.log
   ```

4. **Reinstall the service:**
   ```bash
   cd launchd
   ./install.sh uninstall
   ./install.sh install
   ```

### Not Seeing Any Activity

**Check these first:**

1. **Is it during work hours?** (Mon-Fri, 9 AM - 6 PM)
   - Most "issues" are just the app respecting work hours
   
2. **Is TMetric Desktop running?**
   ```bash
   uv run tmetric-helper is-running
   ```

3. **Check the logs:**
   ```bash
   tail -f /tmp/tmetric-helper.log
   ```

### Service Keeps Restarting

This **shouldn't** happen because the service is configured with `SuccessfulExit: false`, which means it only restarts on crashes (non-zero exit codes). 

If you see it restarting:
1. Check if the app is crashing (check error log)
2. Verify you're during work hours (Mon-Fri, 9 AM - 6 PM)

### Can't See Logs

The logs might not exist if:
- The service hasn't run yet
- You're outside work hours (it exits before writing much)

**Try running manually to see output:**
```bash
uv run tmetric-helper auto-keep-active
```

### Testing Outside Work Hours

To test the service behavior immediately without waiting for work hours:

```bash
# Temporarily modify the work hours check in src/tmetric_helper/cli.py
# Change is_work_hours() to return True

# Then restart the service
cd launchd
./install.sh restart
```

**Remember to revert the changes after testing!**

### Wrong Work Hours

If you need different work hours than the default (9 AM - 6 PM, Mon-Fri), see the [Customizing Work Hours](#customizing-work-hours) section above.

## Manual Background Execution

If you prefer not to use the LaunchAgent service, you can run in the background manually:

```bash
# Using nohup
nohup uv run tmetric-helper auto-keep-active > tmetric-helper.log 2>&1 &

# Check if running
ps aux | grep tmetric-helper

# Stop
pkill -f 'tmetric-helper'

# View logs
tail -f tmetric-helper.log
```

**Note:** When running manually, the app will exit if it's outside work hours. You'll need to start it manually during work hours.

## Development

**Format code with ruff:**
```bash
uv run ruff format .
```

**Lint code:**
```bash
uv run ruff check .
```

**Fix linting issues:**
```bash
uv run ruff check --fix .
```

**Run tests:**
```bash
uv run python test_work_hours.py
```

## Requirements

- Python 3.14 or higher
- macOS (uses PyAutoGUI which supports macOS, Windows, and Linux)
- `uv` for dependency management

## Security & Privacy

### Required Permissions

TMetric Helper needs the following macOS permissions:

1. **Accessibility**: To simulate mouse movements and keyboard input
2. **Input Monitoring**: To detect system idle time

You'll be prompted to grant these when you first run the app.

### What Data is Collected?

**None.** TMetric Helper:
- ✅ Runs entirely locally on your machine
- ✅ Does not send any data anywhere
- ✅ Does not collect or store personal information
- ✅ Only monitors: system idle time and process list

## Dependencies

- `pyautogui` - Cross-platform GUI automation
- `click` - Command-line interface creation kit
- `psutil` - Process and system monitoring
- `ruff` - Python linter and formatter (dev dependency)
- `pyinstaller` - Create standalone executables (dev dependency)

## Safety Note

⚠️ **Warning**: This tool controls your mouse and keyboard. Use with caution:
- Move your mouse to a corner to interrupt PyAutoGUI's fail-safe
- Test commands carefully before using in production
- Be aware of what applications are active when running commands

## Tips & Best Practices

1. **Always check work hours first** - Most "issues" are just the app respecting work hours
2. **Logs are your friend** - Check `/tmp/tmetric-helper.log` when in doubt
3. **Use the install script** - `launchd/install.sh` handles all service management
4. **Test manually first** - Run commands with `uv run` before relying on the service
5. **Service runs automatically** - No need to manually start after installation
6. **Checks every 30 minutes** - Service will self-start when work hours begin

## Quick Reference

```bash
# Installation
uv sync
cd launchd && ./install.sh install

# Service Management
cd launchd
./install.sh status          # Check status
./install.sh logs            # View logs
./install.sh restart         # Restart service
./install.sh uninstall       # Remove service

# Manual Testing
uv run tmetric-helper position              # Get mouse position
uv run tmetric-helper is-running            # Check if TMetric is running
uv run tmetric-helper auto-keep-active      # Run manually (foreground)

# View Logs
tail -f /tmp/tmetric-helper.log            # Watch logs in real-time
tail -f /tmp/tmetric-helper.error.log      # Watch errors

# Service Control (launchctl)
launchctl list | grep tmetric-helper       # Check if loaded
launchctl start com.bukitoka.tmetric-helper   # Start now
launchctl stop com.bukitoka.tmetric-helper    # Stop now
```

## License

MIT