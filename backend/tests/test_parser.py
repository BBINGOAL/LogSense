import unittest

from backend.app.parsing.parser import LogParseError, parse_log_record

class TestParseLogRecord(unittest.TestCase):
    def test_returns_normalized_record_for_valid_json(self):
        raw_line = (
            '{"timestamp":"2026-09-22T10:00:00+07:00",'
            '"service":"auth","level":"info","message":"login succeeded",'
            '"request_id":"req-123","status_code":200,"latency_ms":42.5}'
        )

        record = parse_log_record(raw_line)

        self.assertEqual(
            record.timestamp.isoformat(),
            "2026-09-22T03:00:00+00:00",
        )
        self.assertEqual(record.service, "auth")
        self.assertEqual(record.level, "INFO")
        self.assertEqual(record.message, "login succeeded")
        self.assertEqual(record.request_id, "req-123")
        self.assertEqual(record.status_code, 200)
        self.assertEqual(record.latency_ms, 42.5)

    def test_raises_log_parse_error_for_malformed_json(self):
        raw_line = '{"timestamp":"2026-09-22T10:00:00Z"'
        with self.assertRaisesRegex(LogParseError, "invalid JSON"):
            parse_log_record(raw_line)
            
    def test_raises_log_parse_error_for_missing_timestamp(self):
        raw_line = (
            '{"service":"auth","level":"ERROR",'
            '"message":"login failed"}'
        )

        with self.assertRaisesRegex(
            LogParseError,
            "missing required field: timestamp",
        ):
            parse_log_record(raw_line)
    def test_raises_log_parse_error_for_invalid_timestamp(self):
        raw_line = (
            '{"timestamp":"not-a-timestamp","service":"auth",'
            '"level":"ERROR","message":"login failed"}'
        )

        with self.assertRaisesRegex(LogParseError, "invalid timestamp"):
            parse_log_record(raw_line)

    def test_raises_log_parse_error_when_timestamp_has_no_timezone(self):
        raw_line = (
            '{"timestamp":"2026-09-22T10:00:00","service":"auth",'
            '"level":"ERROR","message":"login failed"}'
        )

        with self.assertRaisesRegex(
            LogParseError,
            "timestamp must include timezone",
        ):
            parse_log_record(raw_line)
if __name__ == "__main__":
    unittest.main()