import unittest
from datetime import datetime, timedelta, timezone

import pandas as pd

from backend.app.incidents.grouping import (
    group_anomalies_into_incidents,
)


class TestGroupAnomaliesIntoIncidents(unittest.TestCase):
    def test_groups_nearby_anomalies_and_splits_large_gap(self):
        started_at = datetime(
            2026,
            9,
            26,
            10,
            0,
            tzinfo=timezone.utc,
        )
        detections = pd.DataFrame(
            {
                "window_start": [
                    started_at,
                    started_at + timedelta(minutes=5),
                    started_at + timedelta(minutes=7),
                    started_at + timedelta(minutes=20),
                ],
                "service": ["auth"] * 4,
                "is_anomaly": [True, True, False, True],
                "anomaly_reason": [
                    "high_error_rate",
                    "high_latency",
                    None,
                    "high_error_rate",
                ],
            }
        )

        incidents = group_anomalies_into_incidents(detections)

        self.assertEqual(len(incidents), 2)

        first = incidents[0]
        self.assertEqual(first.started_at, started_at)
        self.assertEqual(
            first.ended_at,
            started_at + timedelta(minutes=5),
        )
        self.assertEqual(first.severity, "medium")
        self.assertEqual(first.anomaly_count, 2)
        self.assertEqual(first.evidence_indices, (0, 1))
        self.assertEqual(
            first.triggers,
            ("high_error_rate", "high_latency"),
        )

        second = incidents[1]
        self.assertEqual(second.severity, "low")
        self.assertEqual(second.anomaly_count, 1)
        self.assertEqual(second.evidence_indices, (3,))


if __name__ == "__main__":
    unittest.main()