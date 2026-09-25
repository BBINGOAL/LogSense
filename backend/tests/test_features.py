import unittest
from datetime import datetime, timezone

from backend.app.metrics.dataframe import records_to_dataframe
from backend.app.metrics.features import build_request_count_metrics
from backend.app.parsing.models import NormalizedLogRecord


class TestBuildRequestCountMetrics(unittest.TestCase):
    def test_counts_logs_in_five_minute_windows(self):
        records = [
            NormalizedLogRecord(
                timestamp=datetime(
                    2026, 9, 22, 10, 1, tzinfo=timezone.utc
                ),
                service="auth",
                level="INFO",
                message="request 1",
            ),
            NormalizedLogRecord(
                timestamp=datetime(
                    2026, 9, 22, 10, 4, tzinfo=timezone.utc
                ),
                service="auth",
                level="ERROR",
                message="request 2",
            ),
            NormalizedLogRecord(
                timestamp=datetime(
                    2026, 9, 22, 10, 6, tzinfo=timezone.utc
                ),
                service="auth",
                level="INFO",
                message="request 3",
            ),
        ]
        frame = records_to_dataframe(records)

        metrics = build_request_count_metrics(frame)

        self.assertEqual(
            metrics["request_count"].tolist(),
            [2, 1],
        )
        self.assertEqual(
            [
                timestamp.isoformat()
                for timestamp in metrics["window_start"]
            ],
            [
                "2026-09-22T10:00:00+00:00",
                "2026-09-22T10:05:00+00:00",
            ],
        )


if __name__ == "__main__":
    unittest.main()