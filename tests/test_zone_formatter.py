import unittest
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to sys.path (do this at the very top)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utils import formatted_zone


# TEST DATA
july_1_midnight = "2025-07-01T00:00:01"
july_1_midday = "2025-07-01T12:00:01"
july_1_3pm = "2025-07-01T03:00:01"
every_week_and_day_zone = {
    "cnn": "207101",
    "corridor": "03rd St",
    "blockside": "East",
    "line": {},
    "Wed": [{"weeks": [1, 1, 1, 1, 1], "fromHour": "2", "toHour": "6"}],
    "Fri": [{"weeks": [1, 1, 1, 1, 1], "fromHour": "2", "toHour": "6"}],
    "Tues": [{"weeks": [1, 1, 1, 1, 1], "fromHour": "2", "toHour": "6"}],
    "Mon": [{"weeks": [1, 1, 1, 1, 1], "fromHour": "2", "toHour": "6"}],
    "Sun": [{"weeks": [1, 1, 1, 1, 1], "fromHour": "2", "toHour": "6"}],
    "Sat": [{"weeks": [1, 1, 1, 1, 1], "fromHour": "2", "toHour": "6"}],
    "Thu": [{"weeks": [1, 1, 1, 1, 1], "fromHour": "2", "toHour": "6"}],
}


class TestFormatZoneStrings(unittest.TestCase):
    def test_works_for_same_day(self):
        f = formatted_zone(
            every_week_and_day_zone, datetime.fromisoformat(july_1_midnight)
        )
        self.assertIn("03rd St - (E): Tuesday, July 01: 2am-6am (TODAY!)", f)

    def test_skips_same_day_if_end_hour_passed(self):
        f = formatted_zone(
            every_week_and_day_zone, datetime.fromisoformat(july_1_midday)
        )
        self.assertIn("03rd St - (E): Wednesday, July 02: 2am-6am (TOMORROW!)", f)

    def test_works_if_currently_active(self):
        f = formatted_zone(every_week_and_day_zone, datetime.fromisoformat(july_1_3pm))
        self.assertIn("03rd St - (E): Tuesday, July 01: 2am-6am (NOW!)", f)


if __name__ == "__main__":
    unittest.main()
