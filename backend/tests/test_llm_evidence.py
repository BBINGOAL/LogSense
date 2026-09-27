import unittest
from datetime import datetime, timezone

import pandas as pd

from backend.app.incidents.models import Incident
from backend.app.llm_analysis.evidence import (
    REQUIRED_EVIDENCE_COLUMNS,
    build_evidence_bundle,
)


class TestBuildEvidenceBundle(unittest.TestCase):
    def test_uses_only_incident_evidence_rows(self):
        timestamp = datetime(
            2026,
            9,
            27,
            10,
            0,
            tzinfo=timezone.utc,
        )
        detections = pd.DataFrame(
            {
                "window_start": [timestamp, timestamp],
                "service": ["auth", "auth"],
                "request_count": [10, 20],
                "error_count": [1, 12],
                "error_rate": [0.1, 0.6],
                "mean_latency_ms": [100.0, 180.0],
                "p95_latency_ms": [150.0, None],
                "anomaly_reason": [
                    None,
                    "high_error_rate",
                ],
            },
            index=[10, 11],
        )
        incident = Incident(
            incident_id="auth-20260927T100000Z",
            service="auth",
            started_at=timestamp,
            ended_at=timestamp,
            severity="low",
            triggers=("high_error_rate",),
            evidence_indices=(11,),
        )

        bundle = build_evidence_bundle(
            incident,
            detections,
            detector_name="rule_based",
        )

        self.assertEqual(bundle.metric_window_count, 1)

        metric = bundle.metric_windows[0]
        self.assertEqual(metric.request_count, 20)
        self.assertEqual(metric.error_count, 12)
        self.assertEqual(metric.error_rate, 0.6)
        self.assertIsNone(metric.p95_latency_ms)
        self.assertIsNone(metric.anomaly_score)

    def test_rejects_missing_evidence_index(self):
        timestamp = datetime(
            2026,
            9,
            27,
            10,
            0,
            tzinfo=timezone.utc,
        )
        detections = pd.DataFrame(
            columns=REQUIRED_EVIDENCE_COLUMNS,
        )
        incident = Incident(
            incident_id="auth-20260927T100000Z",
            service="auth",
            started_at=timestamp,
            ended_at=timestamp,
            severity="low",
            triggers=("high_error_rate",),
            evidence_indices=(99,),
        )

        with self.assertRaisesRegex(
            ValueError,
            "missing evidence indices",
        ):
            build_evidence_bundle(
                incident,
                detections,
                detector_name="rule_based",
            )


if __name__ == "__main__":
    unittest.main()