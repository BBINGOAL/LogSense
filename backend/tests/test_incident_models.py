import unittest
from datetime import datetime, timedelta, timezone

from backend.app.incidents.models import Incident


class TestIncident(unittest.TestCase):
    def test_stores_incident_fields_and_counts_evidence(self):
        started_at = datetime(
            2026,
            9,
            26,
            10,
            0,
            tzinfo=timezone.utc,
        )
        ended_at = started_at + timedelta(minutes=5)

        incident = Incident(
            incident_id="auth-20260926T100000Z",
            service="auth",
            started_at=started_at,
            ended_at=ended_at,
            severity="high",
            triggers=(
                "high_error_rate",
                "high_latency",
            ),
            evidence_indices=(3, 4),
        )

        self.assertEqual(
            incident.incident_id,
            "auth-20260926T100000Z",
        )
        self.assertEqual(incident.service, "auth")
        self.assertEqual(incident.status, "open")
        self.assertEqual(incident.anomaly_count, 2)
        self.assertEqual(
            incident.triggers,
            ("high_error_rate", "high_latency"),
        )


if __name__ == "__main__":
    unittest.main()