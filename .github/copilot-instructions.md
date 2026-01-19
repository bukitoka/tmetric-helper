<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# TMetric Helper - Project Setup Complete

This is a manual-run Python CLI tool for mouse movement and keyboard typing automation on macOS.

## Project Structure

- **CLI Framework**: click
- **Automation**: pyautogui
- **Package Manager**: uv
- **Linter/Formatter**: ruff

## Key Features

- Manual execution (no automatic scheduling)
- Mouse movement and click automation
- Keyboard typing and key pressing
- System activity monitoring
- Keep-alive functionality to prevent system sleep

## Usage

Run commands manually using `uv run tmetric-helper [command]`

## Notes

- No work hours detection (runs anytime when invoked)
- No launchd/background service (manual execution only)
- No process monitoring (removed TMetric detection)
- All commands available via CLI interface
