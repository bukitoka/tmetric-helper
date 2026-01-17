"""CLI module for TMetric Helper."""

import subprocess
import time
from datetime import datetime

import click
import psutil
import pyautogui

# Configure PyAutoGUI
pyautogui.FAILSAFE = True  # Move mouse to corner to abort


def get_system_idle_time():
    """Get the system idle time in seconds (macOS).

    Returns the time in seconds since the last user input (mouse or keyboard).
    Returns 0 if unable to determine idle time.
    """
    try:
        # Use ioreg to get system idle time on macOS
        result = subprocess.run(
            ["ioreg", "-c", "IOHIDSystem"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Parse the output to find HIDIdleTime
        for line in result.stdout.split("\n"):
            if "HIDIdleTime" in line:
                # Extract the nanoseconds value
                idle_ns = int(line.split("=")[1].strip())
                # Convert nanoseconds to seconds
                return idle_ns / 1_000_000_000

        return 0
    except (subprocess.CalledProcessError, ValueError, IndexError):
        # Fallback to 0 if unable to get idle time
        return 0


@click.group()
@click.version_option()
def cli():
    """TMetric Helper - Automate mouse movements and keyboard typing."""
    pass


@cli.command()
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.option("--duration", "-d", default=1.0, help="Duration of movement in seconds")
def move(x, y, duration):
    """Move mouse to coordinates (X, Y)."""
    click.echo(f"Moving mouse to ({x}, {y}) over {duration}s")
    pyautogui.moveTo(x, y, duration=duration)
    click.echo("✓ Mouse moved successfully")


@cli.command()
@click.argument("text")
@click.option("--interval", "-i", default=0.1, help="Interval between keystrokes in seconds")
@click.option("--delay", "-d", default=0, help="Delay before typing starts in seconds")
def type_text(text, interval, delay):
    """Type TEXT automatically."""
    if delay > 0:
        click.echo(f"Waiting {delay}s before typing...")
        time.sleep(delay)

    click.echo(f"Typing: {text}")
    pyautogui.write(text, interval=interval)
    click.echo("✓ Text typed successfully")


@cli.command()
@click.option("--x", type=int, help="X coordinate to click")
@click.option("--y", type=int, help="Y coordinate to click")
@click.option("--clicks", "-c", default=1, help="Number of clicks")
@click.option("--button", "-b", default="left", type=click.Choice(["left", "right", "middle"]))
def click_at(x, y, clicks, button):
    """Click at specified coordinates or current position."""
    if x is not None and y is not None:
        click.echo(f"Clicking at ({x}, {y}) {clicks} time(s) with {button} button")
        pyautogui.click(x, y, clicks=clicks, button=button)
    else:
        pos = pyautogui.position()
        click.echo(
            f"Clicking at current position ({pos.x}, {pos.y}) {clicks} time(s) with {button} button"
        )
        pyautogui.click(clicks=clicks, button=button)

    click.echo("✓ Click completed successfully")


@cli.command()
@click.argument("key")
@click.option("--presses", "-p", default=1, help="Number of times to press the key")
def press(key, presses):
    """Press a keyboard KEY."""
    click.echo(f"Pressing '{key}' {presses} time(s)")
    for _ in range(presses):
        pyautogui.press(key)
    click.echo("✓ Key press completed successfully")


@cli.command()
def position():
    """Get current mouse position."""
    pos = pyautogui.position()
    click.echo(f"Current mouse position: X={pos.x}, Y={pos.y}")


@cli.command()
@click.argument("commands", nargs=-1)
@click.option("--delay", "-d", default=1.0, help="Delay between commands in seconds")
def sequence(commands, delay):
    """Execute a SEQUENCE of commands.

    Example: tmetric-helper sequence "move:100,200" "click" "type:hello"
    """
    click.echo(f"Executing {len(commands)} commands with {delay}s delay between each")

    for i, cmd in enumerate(commands, 1):
        click.echo(f"\n[{i}/{len(commands)}] Executing: {cmd}")

        parts = cmd.split(":", 1)
        action = parts[0].lower()

        if action == "move" and len(parts) > 1:
            coords = parts[1].split(",")
            if len(coords) == 2:
                x, y = int(coords[0]), int(coords[1])
                pyautogui.moveTo(x, y, duration=0.5)
                click.echo(f"  ✓ Moved to ({x}, {y})")

        elif action == "click":
            pyautogui.click()
            click.echo("  ✓ Clicked")

        elif action == "type" and len(parts) > 1:
            text = parts[1]
            pyautogui.write(text, interval=0.1)
            click.echo(f"  ✓ Typed: {text}")

        elif action == "press" and len(parts) > 1:
            key = parts[1]
            pyautogui.press(key)
            click.echo(f"  ✓ Pressed: {key}")

        elif action == "wait" and len(parts) > 1:
            wait_time = float(parts[1])
            time.sleep(wait_time)
            click.echo(f"  ✓ Waited {wait_time}s")

        else:
            click.echo(f"  ✗ Unknown command: {cmd}")

        if i < len(commands):
            time.sleep(delay)

    click.echo("\n✓ Sequence completed successfully")


@cli.command()
@click.option(
    "--inactivity-timeout",
    "-t",
    default=300,
    help="Seconds of inactivity before action (default: 300 = 5 minutes)",
)
@click.option(
    "--action",
    "-a",
    default="move",
    type=click.Choice(["move", "jiggle", "press"]),
    help="Action to perform: move (small movement), jiggle (wiggle mouse), press (shift key)",
)
@click.option(
    "--check-interval",
    "-i",
    default=10,
    help="Seconds between activity checks (default: 10)",
)
def keep_active(inactivity_timeout, action, check_interval):
    """Monitor for inactivity and perform actions to keep system active.

    This command runs continuously and monitors both mouse and keyboard activity.
    If no activity is detected for the specified timeout period, it will perform
    an action to simulate activity.

    Press Ctrl+C to stop monitoring.
    """
    click.echo("=" * 60)
    click.echo("TMetric Helper - Keep Active Monitor")
    click.echo("=" * 60)
    click.echo(f"Inactivity timeout: {inactivity_timeout}s ({inactivity_timeout // 60} minutes)")
    click.echo(f"Action on inactivity: {action}")
    click.echo(f"Check interval: {check_interval}s")
    click.echo("Monitoring: Mouse movement AND keyboard activity")
    click.echo("\nMonitoring started. Press Ctrl+C to stop.")
    click.echo("Move mouse to a corner to trigger fail-safe abort.")
    click.echo("-" * 60)

    action_count = 0

    try:
        while True:
            time.sleep(check_interval)

            # Get system idle time (includes both mouse and keyboard activity)
            idle_time = get_system_idle_time()

            # Display status
            timestamp = datetime.now().strftime("%H:%M:%S")
            if idle_time >= inactivity_timeout:
                click.echo(
                    f"[{timestamp}] ⚠️  INACTIVE for {int(idle_time)}s - Performing {action}..."
                )

                # Perform the chosen action
                if action == "move":
                    # Small movement to right and back
                    original_pos = pyautogui.position()
                    pyautogui.moveRel(1, 0, duration=0.1)
                    pyautogui.moveTo(original_pos.x, original_pos.y, duration=0.1)

                elif action == "jiggle":
                    # Jiggle mouse in small circle
                    original_pos = pyautogui.position()
                    pyautogui.moveRel(2, 0, duration=0.1)
                    pyautogui.moveRel(0, 2, duration=0.1)
                    pyautogui.moveRel(-2, 0, duration=0.1)
                    pyautogui.moveRel(0, -2, duration=0.1)
                    pyautogui.moveTo(original_pos.x, original_pos.y, duration=0.1)

                elif action == "press":
                    # Press and release shift key (doesn't type anything)
                    pyautogui.press("shift")

                action_count += 1

                click.echo(f"[{timestamp}] ✓ Action completed (total actions: {action_count})")

            else:
                remaining = int(inactivity_timeout - idle_time)
                mouse_pos = pyautogui.position()
                click.echo(
                    f"[{timestamp}] Active - Idle: {int(idle_time)}s - "
                    f"Mouse: ({mouse_pos.x}, {mouse_pos.y}) - Timeout in {remaining}s"
                )

    except KeyboardInterrupt:
        click.echo("\n" + "-" * 60)
        click.echo(f"✓ Monitoring stopped. Total actions performed: {action_count}")
        click.echo("=" * 60)


@cli.command()
@click.option(
    "--process-name",
    "-p",
    default="TMetric Desktop",
    help="Process name to monitor (default: TMetric Desktop)",
)
@click.option(
    "--check-interval",
    "-i",
    default=5,
    help="Seconds between process checks (default: 5)",
)
@click.option(
    "--run-once",
    "-o",
    is_flag=True,
    help="Check once and exit, instead of continuously monitoring",
)
def watch(process_name, check_interval, run_once):
    """Monitor for a process.

    This command watches for a specific process (default: TMetric Desktop).
    For automatic mouse movement when TMetric is running, use 'auto-keep-active'.

    Examples:
        # Monitor and notify when TMetric Desktop is running
        tmetric-helper watch

        # Check once if TMetric Desktop is running
        tmetric-helper watch --run-once
    """
    click.echo("=" * 60)
    click.echo("TMetric Helper - Process Monitor")
    click.echo("=" * 60)
    click.echo(f"Watching for process: {process_name}")
    click.echo(f"Check interval: {check_interval}s")
    if run_once:
        click.echo("Mode: Single check")
    else:
        click.echo("Mode: Continuous monitoring")
        click.echo("\nPress Ctrl+C to stop.")
    click.echo("-" * 60)

    def is_process_running(name):
        """Check if a process with the given name is running."""
        name_lower = name.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = proc.info["name"]
                if proc_name:
                    # Use exact match to avoid false positives
                    # (e.g., "tmetric-helper" should not match "TMetric")
                    if proc_name.lower() == name_lower or proc_name.lower() == f"{name_lower}.exe":
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    check_count = 0

    try:
        while True:
            check_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            is_running = is_process_running(process_name)

            if is_running:
                click.echo(f"[{timestamp}] ✓ {process_name} is running")
                if run_once:
                    break
            else:
                click.echo(f"[{timestamp}] ⨯ {process_name} is not running (check #{check_count})")
                if run_once:
                    click.echo(f"\n{process_name} is not currently running.")
                    break

            if not run_once:
                time.sleep(check_interval)

    except KeyboardInterrupt:
        click.echo("\n" + "-" * 60)
        click.echo(f"✓ Monitoring stopped after {check_count} checks")
        click.echo("=" * 60)


@cli.command()
@click.option(
    "--process-name",
    "-p",
    default="TMetric Desktop",
    help="Process name to monitor (default: TMetric Desktop)",
)
@click.option(
    "--inactivity-timeout",
    "-t",
    default=300,
    help="Seconds of inactivity before action (default: 300 = 5 minutes)",
)
@click.option(
    "--action",
    "-a",
    default="move",
    type=click.Choice(["move", "jiggle", "press"]),
    help="Action to perform: move (small movement), jiggle (wiggle mouse), press (shift key)",
)
@click.option(
    "--check-interval",
    "-i",
    default=10,
    help="Seconds between activity checks (default: 10)",
)
@click.option(
    "--process-check-interval",
    default=30,
    help="Seconds between process checks (default: 30)",
)
def auto_keep_active(
    process_name, inactivity_timeout, action, check_interval, process_check_interval
):
    """Automatically keep system active when TMetric Desktop is running.

    This command combines process monitoring with keep-alive functionality.
    It monitors for TMetric Desktop and only performs mouse movements when:
    1. TMetric Desktop is running, AND
    2. No user activity detected for the specified timeout

    Press Ctrl+C to stop monitoring.
    """
    click.echo("=" * 60)
    click.echo("TMetric Helper - Auto Keep Active")
    click.echo("=" * 60)
    click.echo(f"Target process: {process_name}")
    click.echo(f"Inactivity timeout: {inactivity_timeout}s ({inactivity_timeout // 60} minutes)")
    click.echo(f"Action on inactivity: {action}")
    click.echo(f"Activity check interval: {check_interval}s")
    click.echo(f"Process check interval: {process_check_interval}s")
    click.echo("Monitoring: Mouse movement AND keyboard activity")
    click.echo("\nMonitoring started. Press Ctrl+C to stop.")
    click.echo("Move mouse to a corner to trigger fail-safe abort.")
    click.echo("-" * 60)

    def is_process_running(name):
        """Check if a process with the given name is running."""
        name_lower = name.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = proc.info["name"]
                if proc_name:
                    # Use exact match to avoid false positives
                    # (e.g., "tmetric-helper" should not match "TMetric")
                    if proc_name.lower() == name_lower or proc_name.lower() == f"{name_lower}.exe":
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    last_process_check = time.time()
    action_count = 0
    tmetric_running = False

    try:
        while True:
            current_time = time.time()

            # Check if TMetric is running (periodically)
            if current_time - last_process_check >= process_check_interval:
                tmetric_running = is_process_running(process_name)
                timestamp = datetime.now().strftime("%H:%M:%S")
                if tmetric_running:
                    click.echo(f"[{timestamp}] ✓ {process_name} is running - monitoring active")
                else:
                    click.echo(f"[{timestamp}] ⨯ {process_name} not running - skipping monitoring")
                last_process_check = current_time

            # Only monitor activity if TMetric is running
            if tmetric_running:
                time.sleep(check_interval)
                current_time = time.time()

                # Get system idle time (includes both mouse and keyboard activity)
                idle_time = get_system_idle_time()

                # Display status
                timestamp = datetime.now().strftime("%H:%M:%S")
                if idle_time >= inactivity_timeout:
                    click.echo(
                        f"[{timestamp}] ⚠️  INACTIVE for {int(idle_time)}s - Performing {action}..."
                    )

                    # Perform the chosen action
                    if action == "move":
                        original_pos = pyautogui.position()
                        pyautogui.moveRel(1, 0, duration=0.1)
                        pyautogui.moveTo(original_pos.x, original_pos.y, duration=0.1)

                    elif action == "jiggle":
                        original_pos = pyautogui.position()
                        pyautogui.moveRel(2, 0, duration=0.1)
                        pyautogui.moveRel(0, 2, duration=0.1)
                        pyautogui.moveRel(-2, 0, duration=0.1)
                        pyautogui.moveRel(0, -2, duration=0.1)
                        pyautogui.moveTo(original_pos.x, original_pos.y, duration=0.1)

                    elif action == "press":
                        pyautogui.press("shift")

                    action_count += 1

                    click.echo(f"[{timestamp}] ✓ Action completed (total: {action_count})")
                else:
                    remaining = int(inactivity_timeout - idle_time)
                    mouse_pos = pyautogui.position()
                    click.echo(
                        f"[{timestamp}] Active - Idle: {int(idle_time)}s - "
                        f"Mouse: ({mouse_pos.x}, {mouse_pos.y}) - Timeout in {remaining}s"
                    )
            else:
                # TMetric not running, just wait
                time.sleep(process_check_interval)

    except KeyboardInterrupt:
        click.echo("\n" + "-" * 60)
        click.echo(f"✓ Monitoring stopped. Total actions performed: {action_count}")
        click.echo("=" * 60)


@cli.command()
@click.option(
    "--process-name",
    "-p",
    default="TMetric Desktop",
    help="Process name to check (default: TMetric Desktop)",
)
def is_running(process_name):
    """Check if a process is currently running.

    Returns exit code 0 if running, 1 if not running.
    Useful for scripting and automation.
    """
    name_lower = process_name.lower()
    running_processes = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            proc_name = proc.info["name"]
            if proc_name:
                # Use exact match to avoid false positives
                # (e.g., "tmetric-helper" should not match "TMetric")
                if proc_name.lower() == name_lower or proc_name.lower() == f"{name_lower}.exe":
                    running_processes.append((proc.info["pid"], proc_name))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if running_processes:
        click.echo(f"✓ {process_name} is running:")
        for pid, name in running_processes:
            click.echo(f"  PID {pid}: {name}")
        exit(0)
    else:
        click.echo(f"⨯ {process_name} is not running")
        exit(1)


if __name__ == "__main__":
    cli()
