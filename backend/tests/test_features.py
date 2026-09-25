import unittest
from datetime import datetime, timezone

from backend.app.metrics.dataframe import records_to_dataframe
from backend.app.metrics.features import build_window_metrics
from backend.app.parsing.models import NormalizedLogRecord


class TestBuildWindowMetrics(unittest.TestCase):
    def test_counts_logs_in_five_minute_windows(self):
        records = [
            NormalizedLogRecord(
                timestamp=datetime(
                    2026, 9, 22, 10, 1, tzinfo=timezone.utc
                ),
                service="auth",
                level="INFO",
                message="request 1",
                latency_ms=100.0,
            ),
            NormalizedLogRecord(
                timestamp=datetime(
                    2026, 9, 22, 10, 4, tzinfo=timezone.utc
                ),
                service="auth",
                level="ERROR",
                message="request 2",
                latency_ms=200.0,
            ),
            NormalizedLogRecord(
                timestamp=datetime(
                    2026, 9, 22, 10, 6, tzinfo=timezone.utc
                ),
                service="auth",
                level="INFO",
                message="request 3",
                latency_ms=50.0,
            ),
        ]
        frame = records_to_dataframe(records)

        metrics = build_window_metrics(frame)

        self.assertEqual(
            metrics["request_count"].tolist(),
            [2, 1],
        )
        self.assertEqual(
            metrics["error_count"].tolist(),
            [1, 0],
        )
        self.assertEqual(
            metrics["error_rate"].tolist(),
            [0.5, 0.0],
        )
        self.assertEqual(
            metrics["mean_latency_ms"].tolist(),
            [150.0, 50.0],
        )
        self.assertEqual(
            metrics["p95_latency_ms"].tolist(),
            [195.0, 50.0],
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