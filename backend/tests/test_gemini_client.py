import json
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

from backend.app.incidents.models import Incident
from backend.app.llm_analysis.gemini_client import (
    DEFAULT_GEMINI_MODEL,
    analyze_incident_with_gemini,
)
from backend.app.llm_analysis.models import (
    EvidenceBundle,
    MetricEvidence,
)
from backend.app.llm_analysis.response import (
    ANALYSIS_RESPONSE_SCHEMA,
)


class TestAnalyzeIncidentWithGemini(unittest.TestCase):
    def setUp(self):
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
            p95_latency_ms=None,
            anomaly_reason="high_error_rate",
        )
        self.bundle = EvidenceBundle(
            incident=incident,
            detector_name="rule_based",
            metric_windows=(metric,),
        )

    def test_sends_structured_request_and_parses_response(self):
        raw_response = json.dumps({
            "observed_facts": [
                "The auth error rate was 0.6.",
            ],
            "likely_explanation": (
                "Authentication requests may be failing."
            ),
            "uncertainty": (
                "No stack trace was supplied."
            ),
            "recommended_next_checks": [
                "Inspect auth error logs.",
            ],
        })
        create_interaction = Mock(
            return_value=SimpleNamespace(
                output_text=raw_response,
            )
        )

        result = analyze_incident_with_gemini(
            self.bundle,
            create_interaction,
        )

        request = create_interaction.call_args.kwargs
        self.assertEqual(
            request["response_format"]["schema"],
            ANALYSIS_RESPONSE_SCHEMA,
        )
        self.assertFalse(request["store"])
        self.assertIn(
            "auth-20260927T100000Z",
            request["input"],
        )
        self.assertEqual(
            result.response.observed_facts,
            ("The auth error rate was 0.6.",),
        )
        self.assertEqual(
            result.metadata.incident_id,
            "auth-20260927T100000Z",
        )
        self.assertEqual(
            result.metadata.detector_name,
            "rule_based",
        )
        self.assertEqual(
            result.metadata.model,
            DEFAULT_GEMINI_MODEL,
        )
        self.assertEqual(
            result.metadata.prompt_version,
            "incident-analysis-v2",
        )
        self.assertEqual(
            result.metadata.evidence_indices,
            (0,),
        )

    def test_rejects_empty_model_response(self):
        create_interaction = Mock(
            return_value=SimpleNamespace(output_text=""),
        )

        with self.assertRaisesRegex(
            ValueError,
            "empty analysis response",
        ):
            analyze_incident_with_gemini(
                self.bundle,
                create_interaction,
            )


if __name__ == "__main__":
    unittest.main()