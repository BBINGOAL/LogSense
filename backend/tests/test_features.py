import unittest
from datetime import datetime, timezone

from backend.app.metrics.dataframe import records_to_dataframe
from backend.app.metrics.features import (
    METRIC_COLUMNS,
    build_window_metrics,
    )
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
    def test_empty_frame_returns_empty_metric_schema(self):
        frame = records_to_dataframe([])

        metrics = build_window_metrics(frame)

        self.assertTrue(metrics.empty)
        self.assertEqual(
            list(metrics.columns),
            list(METRIC_COLUMNS),
        )
        self.assertEqual(
            str(metrics["window_start"].dt.tz),
            "UTC",
        )
    def test_preserves_counts_when_latency_is_missing(self):
        record = NormalizedLogRecord(
            timestamp=datetime(
                2026,
                9,
                22,
                10,
                1,
                tzinfo=timezone.utc,
            ),
            service="auth",
            level="ERROR",
            message="login failed",
        )
        frame = records_to_dataframe([record])

        metrics = build_window_metrics(frame)

        self.assertEqual(metrics["request_count"].tolist(), [1])
        self.assertEqual(metrics["error_count"].tolist(), [1])
        self.assertEqual(metrics["error_rate"].tolist(), [1.0])
        self.assertTrue(metrics["mean_latency_ms"].isna().all())
        self.assertTrue(metrics["p95_latency_ms"].isna().all())
    def test_groups_metrics_by_service(self):
        timestamp = datetime(
            2026,
            9,
            22,
            10,
            1,
            tzinfo=timezone.utc,
        )
        records = [
            NormalizedLogRecord(
                timestamp=timestamp,
                service="auth",
                level="ERROR",
                message="login failed",
                latency_ms=100.0,
            ),
            NormalizedLogRecord(
                timestamp=timestamp,
                service="payment",
                level="INFO",
                message="payment accepted",
                latency_ms=300.0,
            ),
        ]
        frame = records_to_dataframe(records)

        metrics = build_window_metrics(frame)
        metrics_by_service = metrics.set_index("service")

        self.assertEqual(
            metrics_by_service.loc["auth", "request_count"],
            1,
        )
        self.assertEqual(
            metrics_by_service.loc["auth", "error_count"],
            1,
        )
        self.assertEqual(
            metrics_by_service.loc["auth", "error_rate"],
            1.0,
        )
        self.assertEqual(
            metrics_by_service.loc["payment", "request_count"],
            1,
        )
        self.assertEqual(
            metrics_by_service.loc["payment", "error_count"],
            0,
        )
        self.assertEqual(
            metrics_by_service.loc["payment", "error_rate"],
            0.0,
        )
if __name__ == "__main__":
    unittest.main()