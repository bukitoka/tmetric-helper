# TMetric Helper

A Python CLI tool for automating mouse movements and keyboard typing on macOS.

## Features

- **Mouse Movement**: Move the mouse pointer to specific coordinates
- **Automatic Typing**: Type text automatically with configurable intervals
- **Click Automation**: Click at specific coordinates or current position
- **Key Pressing**: Press keyboard keys programmatically
- **Position Detection**: Get current mouse position
- **Command Sequences**: Execute multiple commands in sequence
- **Keep System Active**: Prevent system sleep/inactivity with automatic mouse movements

## Quick Start

```bash
# Install dependencies
uv sync

# Run the helper
uv run tmetric-helper --help
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

**Running the built binary:**

```bash
# Run directly from dist/
./dist/tmetric-helper position
./dist/tmetric-helper keep-active
./dist/tmetric-helper move 100 200

# Or copy to a directory in your PATH for global access
sudo cp ./dist/tmetric-helper /usr/local/bin/
tmetric-helper --help

# Or create a symbolic link
sudo ln -s $(pwd)/dist/tmetric-helper /usr/local/bin/tmetric-helper
tmetric-helper position
```

**Note**: Building the executable is optional; you can use `uv run tmetric-helper` directly. The built binary is self-contained and doesn't require Python or uv to be installed.

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

## Configuration
   cd launchd
   ./install.sh uninstall
   ./install.sh install
   ```

### Not Seeing Any Activity

**Check these first:**

1. **Is it during work hours?** (Mon-Fri, 9 AM - 6 PM)
   - Most "issues" are just the app respecting work hours
All commands are run manually using `uv run tmetric-helper [command]`. You can customize command parameters as needed. See [Usage](#usage) section for available commands and options.

## Troubleshooting

### Commands Not Working

1. **Ensure dependencies are installed:**
   ```bash
   uv sync
   ```

2. **Test basic commands:**
   ```bash
   uv run tmetric-helper position
   ```

### Mouse Movement Not Working

- Make sure you've granted Accessibility permissions to Terminal/iTerm in System Preferences > Security & Privacy > Privacy > Accessibility
- PyAutoGUI's fail-safe is enabled by default (move mouse to corner to abort)

## Manual Background Execution

If you want to run a command in the background manually:

```bash
# Using nohup
nohup uv run tmetric-helper keep-active > tmetric-helper.log 2>&1 &

# Check if running
ps aux | grep tmetric-helper

# Stop
pkill -f 'tmetric-helper'

# View logs
tail -f tmetric-helper.log
```

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
- ✅ Only monitors: system idle time

## Dependencies

- `pyautogui` - Cross-platform GUI automation
- `click` - Command-line interface creation kit
- `ruff` - Python linter and formatter (dev dependency)
- `pyinstaller` - Create standalone executables (dev dependency)

## Safety Note

⚠️ **Warning**: This tool controls your mouse and keyboard. Use with caution:
- Move your mouse to a corner to interrupt PyAutoGUI's fail-safe
- Test commands carefully before using in production
- Be aware of what applications are active when running commands

## Tips & Best Practices

1. **Test commands manually first** - Always test with `uv run` before automating
2. **Use background execution carefully** - Make sure you can easily stop processes
3. **Accessibility permissions** - Make sure Terminal/iTerm has the required permissions

## Quick Reference

```bash
# Installation
uv sync

# Common Commands
uv run tmetric-helper position              # Get mouse position
uv run tmetric-helper keep-active           # Keep system active (manual run)

# Background Execution (manual)
nohup uv run tmetric-helper keep-active > tmetric-helper.log 2>&1 &
ps aux | grep tmetric-helper                # Check if running
pkill -f 'tmetric-helper'                   # Stop background process
```

## License

MIT