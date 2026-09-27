import os

import pandas as pd
from dotenv import load_dotenv
from google import genai

from backend.app.llm_analysis.gemini_client import (
    DEFAULT_GEMINI_MODEL,
    InteractionCreator,
    analyze_incident_with_gemini,
)
from backend.app.llm_analysis.models import EvidenceBundle
from backend.app.llm_analysis.response import AnalysisResult
from backend.app.incidents.models import Incident
from backend.app.llm_analysis.evidence import build_evidence_bundle


def create_gemini_client() -> genai.Client:
    # Local .env wins over stale values in the terminal.
    load_dotenv(override=True)

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured"
        )

    return genai.Client(api_key=api_key)


def analyze_incident(
    bundle: EvidenceBundle,
    model: str = DEFAULT_GEMINI_MODEL,
    create_interaction: InteractionCreator | None = None,
) -> AnalysisResult:
    if create_interaction is None:
        client = create_gemini_client()
        create_interaction = client.interactions.create

    return analyze_incident_with_gemini(
        bundle,
        create_interaction,
        model,
    )


def analyze_detected_incident(
    incident: Incident,
    detections: pd.DataFrame,
    detector_name: str,
    model: str = DEFAULT_GEMINI_MODEL,
    create_interaction: InteractionCreator | None = None,
) -> AnalysisResult:
    bundle = build_evidence_bundle(
        incident,
        detections,
        detector_name,
    )

    return analyze_incident(
        bundle,
        model,
        create_interaction,
    )