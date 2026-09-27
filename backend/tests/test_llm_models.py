import unittest
from datetime import datetime, timezone

from backend.app.incidents.models import Incident
from backend.app.llm_analysis.models import (
    EvidenceBundle,
    MetricEvidence,
)


class TestEvidenceBundle(unittest.TestCase):
    def test_stores_incident_and_metric_evidence(self):
        timestamp = datetime(
            2026,
            9,
            27,
            10,
            0,
            tzinfo=timezone.utc,
        )
        incident = Incident(
            incident_id="auth-20260927T100000Z",
            service="auth",
            started_at=timestamp,
            ended_at=timestamp,
            severity="low",
            triggers=("high_error_rate",),
            evidence_indices=(0,),
        )
        metric = MetricEvidence(
            window_start=timestamp,
            request_count=20,
            error_count=12,
            error_rate=0.6,
            mean_latency_ms=180.0,
            p95_latency_ms=300.0,
            anomaly_reason="high_error_rate",
        )

        bundle = EvidenceBundle(
            incident=incident,
            detector_name="rule_based",
            metric_windows=(metric,),
        )

        self.assertEqual(
            bundle.incident.incident_id,
            "auth-20260927T100000Z",
        )
        self.assertEqual(bundle.detector_name, "rule_based")
        self.assertEqual(bundle.metric_window_count, 1)
        self.assertEqual(bundle.log_samples, ())
        self.assertIsNone(
            bundle.metric_windows[0].anomaly_score
        )


if __name__ == "__main__":
    unittest.main()