# TMetric Helper

A Python CLI tool for automating mouse movements and keyboard typing on macOS.

## Features

- **Mouse Movement**: Move the mouse pointer to specific coordinates
- **Automatic Typing**: Type text automatically with configurable intervals
- **Click Automation**: Click at specific coordinates or current position
- **Key Pressing**: Press keyboard keys programmatically
- **Position Detection**: Get current mouse position
- **Command Sequences**: Execute multiple commands in sequence

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

### Building Standalone Executable

You can build a standalone executable binary that doesn't require Python to be installed:

```bash
# Install PyInstaller (included in dev dependencies)
uv sync

# Build the executable
uv run python build.py

# The executable will be created in the dist/ directory
./dist/tmetric-helper --help
```

The executable includes all dependencies and can be distributed to other machines without requiring Python installation.

## Usage

### Basic Commands

**Get current mouse position:**
```bash
tmetric-helper position
```

**Move mouse to coordinates:**
```bash
tmetric-helper move 100 200
tmetric-helper move 100 200 --duration 2.0
```

**Type text automatically:**
```bash
tmetric-helper type-text "Hello, World!"
tmetric-helper type-text "Hello" --interval 0.2 --delay 3
```

**Click at coordinates:**
```bash
tmetric-helper click-at --x 100 --y 200
tmetric-helper click-at --x 100 --y 200 --clicks 2 --button right
```

**Press a key:**
```bash
tmetric-helper press enter
tmetric-helper press space --presses 3
```

### Keep System Active

**Monitor for inactivity and perform actions automatically:**
```bash
# Default: Move mouse after 5 minutes of inactivity
tmetric-helper keep-active

# Custom timeout (e.g., 3 minutes = 180 seconds)
tmetric-helper keep-active --inactivity-timeout 180

# Different actions
tmetric-helper keep-active --action jiggle  # Wiggle mouse in circle
tmetric-helper keep-active --action press   # Press shift key

# Custom check interval (check every 30 seconds)
tmetric-helper keep-active --check-interval 30
```

The `keep-active` command runs continuously and monitors mouse movement. When no activity is detected for the specified timeout period (default: 5 minutes), it performs a subtle action to keep the system active. Press Ctrl+C to stop monitoring.

### Advanced: Command Sequences

Execute multiple commands in sequence:

```bash
tmetric-helper sequence "move:100,200" "click" "type:hello" "press:enter"
```

Available sequence commands:
- `move:x,y` - Move mouse to coordinates
- `click` - Click at current position
- `type:text` - Type text
- `press:key` - Press a key
- `wait:seconds` - Wait for specified seconds

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

- Python 3.10 or higher
- macOS (uses PyAutoGUI which supports macOS, Windows, and Linux)

## Dependencies

- `pyautogui` - Cross-platform GUI automation
- `click` - Command-line interface creation kit
- `ruff` - Python linter and formatter (dev dependency)

## Safety Note

⚠️ **Warning**: This tool controls your mouse and keyboard. Use with caution:
- Move your mouse to a corner to interrupt PyAutoGUI's fail-safe
- Test commands carefully before using in production
- Be aware of what applications are active when running commands

## License

MIT
