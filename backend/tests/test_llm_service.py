import os
import unittest
from unittest.mock import Mock, patch

from backend.app.llm_analysis.gemini_client import (
    DEFAULT_GEMINI_MODEL,
)
from backend.app.llm_analysis.models import EvidenceBundle
from backend.app.llm_analysis.response import AnalysisResponse
from backend.app.llm_analysis.service import (
    analyze_incident,
    create_gemini_client,
)


class TestCreateGeminiClient(unittest.TestCase):
    def test_creates_client_from_environment_key(self):
        fake_client = object()

        with (
            patch.dict(
                os.environ,
                {"GEMINI_API_KEY": "test-key"},
                clear=True,
            ),
            patch(
                "backend.app.llm_analysis.service.load_dotenv"
            ),
            patch(
                "backend.app.llm_analysis.service.genai.Client",
                return_value=fake_client,
            ) as client_class,
        ):
            result = create_gemini_client()

        self.assertIs(result, fake_client)
        client_class.assert_called_once_with(
            api_key="test-key"
        )

    def test_rejects_missing_environment_key(self):
        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "backend.app.llm_analysis.service.load_dotenv"
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "GEMINI_API_KEY is not configured",
            ):
                create_gemini_client()


class TestAnalyzeIncidentService(unittest.TestCase):
    def test_delegates_to_injected_interaction_creator(self):
        bundle = Mock(spec=EvidenceBundle)
        create_interaction = Mock()
        expected = AnalysisResponse(
            observed_facts=("A fact.",),
            likely_explanation="A possible explanation.",
            uncertainty="Evidence is limited.",
            recommended_next_checks=("Check logs.",),
        )

        with patch(
            "backend.app.llm_analysis.service."
            "analyze_incident_with_gemini",
            return_value=expected,
        ) as adapter:
            result = analyze_incident(
                bundle,
                create_interaction=create_interaction,
            )

        self.assertEqual(result, expected)
        adapter.assert_called_once_with(
            bundle,
            create_interaction,
            DEFAULT_GEMINI_MODEL,
        )


if __name__ == "__main__":
    unittest.main()