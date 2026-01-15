"""CLI module for TMetric Helper."""

import time
from datetime import datetime

import click
import pyautogui

# Configure PyAutoGUI
pyautogui.FAILSAFE = True  # Move mouse to corner to abort


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

    This command runs continuously and monitors mouse position. If no mouse
    movement is detected for the specified timeout period, it will perform
    an action to simulate activity.

    Press Ctrl+C to stop monitoring.
    """
    click.echo("=" * 60)
    click.echo("TMetric Helper - Keep Active Monitor")
    click.echo("=" * 60)
    click.echo(f"Inactivity timeout: {inactivity_timeout}s ({inactivity_timeout // 60} minutes)")
    click.echo(f"Action on inactivity: {action}")
    click.echo(f"Check interval: {check_interval}s")
    click.echo("\nMonitoring started. Press Ctrl+C to stop.")
    click.echo("Move mouse to a corner to trigger fail-safe abort.")
    click.echo("-" * 60)

    last_position = pyautogui.position()
    last_activity_time = time.time()
    action_count = 0

    try:
        while True:
            time.sleep(check_interval)
            current_position = pyautogui.position()
            current_time = time.time()

            # Check if mouse has moved
            if current_position != last_position:
                last_position = current_position
                last_activity_time = current_time
                inactive_duration = 0
            else:
                inactive_duration = current_time - last_activity_time

            # Display status
            timestamp = datetime.now().strftime("%H:%M:%S")
            if inactive_duration >= inactivity_timeout:
                click.echo(
                    f"[{timestamp}] ⚠️  INACTIVE for {int(inactive_duration)}s - Performing {action}..."
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
                last_activity_time = current_time
                last_position = pyautogui.position()

                click.echo(f"[{timestamp}] ✓ Action completed (total actions: {action_count})")

            else:
                remaining = int(inactivity_timeout - inactive_duration)
                click.echo(
                    f"[{timestamp}] Active - Position: ({current_position.x}, {current_position.y}) "
                    f"- Next check in {check_interval}s (timeout in {remaining}s)"
                )

    except KeyboardInterrupt:
        click.echo("\n" + "-" * 60)
        click.echo(f"✓ Monitoring stopped. Total actions performed: {action_count}")
        click.echo("=" * 60)


if __name__ == "__main__":
    cli()
