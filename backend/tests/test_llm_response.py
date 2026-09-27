import json
import unittest

from backend.app.llm_analysis.response import (
    AnalysisMetadata,
    AnalysisResponse,
    AnalysisResult,
    parse_analysis_response,
)


class TestParseAnalysisResponse(unittest.TestCase):
    def test_returns_typed_response_for_valid_json(self):
        raw_response = json.dumps({
            "observed_facts": [
                "The auth service error rate was 0.6.",
            ],
            "likely_explanation": (
                "Authentication requests may be failing."
            ),
            "uncertainty": (
                "The evidence does not include a stack trace."
            ),
            "recommended_next_checks": [
                "Inspect auth service error logs.",
            ],
        })

        result = parse_analysis_response(raw_response)

        self.assertIsInstance(result, AnalysisResponse)
        self.assertEqual(
            result.observed_facts,
            ("The auth service error rate was 0.6.",),
        )
        self.assertEqual(
            result.recommended_next_checks,
            ("Inspect auth service error logs.",),
        )

    def test_rejects_invalid_json(self):
        with self.assertRaisesRegex(
            ValueError,
            "not valid JSON",
        ):
            parse_analysis_response("{invalid json}")

    def test_rejects_missing_required_field(self):
        raw_response = json.dumps({
            "observed_facts": [],
            "likely_explanation": "Possible auth failure.",
            "uncertainty": "No stack trace is available.",
        })

        with self.assertRaisesRegex(
            ValueError,
            "recommended_next_checks",
        ):
            parse_analysis_response(raw_response)

    def test_rejects_wrong_field_type(self):
        raw_response = json.dumps({
            "observed_facts": "Error rate was 0.6.",
            "likely_explanation": "Possible auth failure.",
            "uncertainty": "No stack trace is available.",
            "recommended_next_checks": [],
        })

        with self.assertRaisesRegex(
            ValueError,
            "observed_facts must be a list",
        ):
            parse_analysis_response(raw_response)


class TestAnalysisResult(unittest.TestCase):
    def test_stores_response_with_traceability_metadata(self):
        metadata = AnalysisMetadata(
            incident_id="auth-20260927T100000Z",
            detector_name="rule_based",
            model="gemini-3.8-flash",
            prompt_version="incident-analysis-v2",
            evidence_indices=(7, 8),
        )
        response = AnalysisResponse(
            observed_facts=("The error rate was 0.6.",),
            likely_explanation="Requests may be failing.",
            uncertainty="No stack trace was supplied.",
            recommended_next_checks=("Inspect error logs.",),
        )

        result = AnalysisResult(
            metadata=metadata,
            response=response,
        )

        self.assertEqual(
            result.metadata.incident_id,
            "auth-20260927T100000Z",
        )
        self.assertEqual(result.metadata.evidence_count, 2)
        self.assertIs(result.response, response)


if __name__ == "__main__":
    unittest.main()
