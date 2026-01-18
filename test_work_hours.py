"""Test script to verify work hours check functionality."""

from datetime import datetime
from unittest.mock import patch

from src.tmetric_helper.cli import is_work_hours


def test_work_hours():
    """Test various scenarios for work hours check."""

    test_cases = [
        # (year, month, day, hour, minute, expected, description)
        (2026, 1, 19, 9, 0, True, "Monday 9:00 AM - Start of work hours"),
        (2026, 1, 19, 12, 0, True, "Monday 12:00 PM - Middle of work hours"),
        (2026, 1, 19, 17, 59, True, "Monday 5:59 PM - End of work hours"),
        (2026, 1, 19, 18, 0, False, "Monday 6:00 PM - After work hours"),
        (2026, 1, 19, 8, 59, False, "Monday 8:59 AM - Before work hours"),
        (2026, 1, 19, 3, 0, False, "Monday 3:00 AM - Early morning"),
        (2026, 1, 19, 21, 0, False, "Monday 9:00 PM - Evening"),
        (2026, 1, 20, 10, 0, True, "Tuesday 10:00 AM - Work hours"),
        (2026, 1, 21, 14, 30, True, "Wednesday 2:30 PM - Work hours"),
        (2026, 1, 22, 16, 0, True, "Thursday 4:00 PM - Work hours"),
        (2026, 1, 23, 11, 0, True, "Friday 11:00 AM - Work hours"),
        (2026, 1, 24, 10, 0, False, "Saturday 10:00 AM - Weekend"),
        (2026, 1, 25, 14, 0, False, "Sunday 2:00 PM - Weekend"),
        (2026, 1, 24, 3, 0, False, "Saturday 3:00 AM - Weekend early morning"),
        (2026, 1, 25, 20, 0, False, "Sunday 8:00 PM - Weekend evening"),
    ]

    print("Testing work hours check functionality")
    print("=" * 70)

    passed = 0
    failed = 0

    for year, month, day, hour, minute, expected, description in test_cases:
        test_datetime = datetime(year, month, day, hour, minute)

        with patch("src.tmetric_helper.cli.datetime") as mock_datetime:
            mock_datetime.now.return_value = test_datetime
            result = is_work_hours()

            status = "✓ PASS" if result == expected else "✗ FAIL"
            if result == expected:
                passed += 1
            else:
                failed += 1

            print(f"{status} | {description}")
            print(f"      Expected: {expected}, Got: {result}")
            print(f"      Date: {test_datetime.strftime('%A, %Y-%m-%d %I:%M %p')}")
            print()

    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")

    if failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {failed} test(s) failed!")
        return 1


if __name__ == "__main__":
    exit(test_work_hours())
