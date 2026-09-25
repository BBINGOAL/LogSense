import unittest
from datetime import datetime, timezone

from backend.app.metrics.dataframe import LOG_COLUMNS, records_to_dataframe
from backend.app.parsing.models import NormalizedLogRecord


class TestRecordsToDataFrame(unittest.TestCase):
    def test_creates_row_from_normalized_record(self):
        timestamp = datetime(
            2026,
            9,
            22,
            10,
            0,
            tzinfo=timezone.utc,
        )
        record = NormalizedLogRecord(
            timestamp=timestamp,
            service="auth",
            level="ERROR",
            message="login failed",
            request_id="req-123",
            status_code=401,
            latency_ms=42.5,
        )

        frame = records_to_dataframe([record])

        self.assertEqual(frame.shape, (1, 7))
        self.assertEqual(list(frame.columns), list(LOG_COLUMNS))
        self.assertEqual(frame.loc[0, "timestamp"], timestamp)
        self.assertEqual(frame.loc[0, "service"], "auth")
        self.assertEqual(frame.loc[0, "level"], "ERROR")
        self.assertEqual(frame.loc[0, "latency_ms"], 42.5)

    def test_empty_records_preserve_columns(self):
        frame = records_to_dataframe([])

        self.assertTrue(frame.empty)
        self.assertEqual(list(frame.columns), list(LOG_COLUMNS))

    def test_assigns_analysis_friendly_dtypes(self):
        record = NormalizedLogRecord(
            timestamp=datetime(
                2026,
                9,
                22,
                10,
                0,
                tzinfo=timezone.utc,
            ),
            service="auth",
            level="INFO",
            message="login succeeded",
        )

        frame = records_to_dataframe([record])

        self.assertEqual(str(frame["timestamp"].dt.tz), "UTC")
        self.assertEqual(str(frame["service"].dtype), "string")
        self.assertEqual(str(frame["level"].dtype), "string")
        self.assertEqual(str(frame["status_code"].dtype), "Int64")
        self.assertEqual(str(frame["latency_ms"].dtype), "Float64")
    
if __name__ == "__main__":
    unittest.main()