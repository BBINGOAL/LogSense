import json
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import pandas as pd

from backend.app.incidents.models import Incident
from backend.app.llm_analysis.service import (
    analyze_detected_incident,
)


class TestLlmPipeline(unittest.TestCase):
    def test_analyzes_detected_incident_end_to_end(self):
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
            evidence_indices=(7,),
        )
        detections = pd.DataFrame(
            {
                "window_start": [timestamp],
                "service": ["auth"],
                "request_count": [20],
                "error_count": [12],
                "error_rate": [0.6],
                "mean_latency_ms": [180.0],
                "p95_latency_ms": [250.0],
                "anomaly_reason": ["high_error_rate"],
            },
            index=[7],
        )

        raw_response = json.dumps({
            "observed_facts": [
                "The auth error rate was 0.6.",
            ],
            "likely_explanation": (
                "Authentication requests may be failing."
            ),
            "uncertainty": (
                "No individual error logs were supplied."
            ),
            "recommended_next_checks": [
                "Inspect authentication error logs.",
            ],
        })
        create_interaction = Mock(
            return_value=SimpleNamespace(
                output_text=raw_response,
            )
        )

        result = analyze_detected_incident(
            incident,
            detections,
            detector_name="rule_based",
            create_interaction=create_interaction,
        )

        request = create_interaction.call_args.kwargs
        prompt_payload = json.loads(request["input"])

        self.assertEqual(
            prompt_payload["prompt_version"],
            "incident-analysis-v1",
        )
        self.assertEqual(
            prompt_payload["evidence"]["incident"]["incident_id"],
            incident.incident_id,
        )
        self.assertEqual(
            prompt_payload["evidence"]["metric_windows"][0][
                "error_rate"
            ],
            0.6,
        )
        self.assertEqual(
            result.observed_facts,
            ("The auth error rate was 0.6.",),
        )
        self.assertFalse(request["store"])


if __name__ == "__main__":
    unittest.main()