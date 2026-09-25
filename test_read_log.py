import unittest

from read_log import parse_timestamp_utc

class TestParseTimestampUtc(unittest.TestCase):
    def test_converts_timestamp_to_utc(self):
        result = parse_timestamp_utc("2026-09-22T10:00:00+07:00")

        self.assertIsNotNone(result)
        self.assertEqual(result.isoformat(), "2026-09-22T03:00:00+00:00")

    def test_returns_none_when_timezone_missing(self):
        result = parse_timestamp_utc("2026-09-22T10:00:00")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()