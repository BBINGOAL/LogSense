from typing import Protocol

from backend.app.llm_analysis.models import EvidenceBundle
from backend.app.llm_analysis.prompt import build_analysis_prompt
from backend.app.llm_analysis.response import (
    ANALYSIS_RESPONSE_SCHEMA,
    AnalysisResponse,
    parse_analysis_response,
)


DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"


class InteractionResult(Protocol):
    output_text: str


class InteractionCreator(Protocol):
    def __call__(
        self,
        **kwargs: object,
    ) -> InteractionResult:
        ...


def analyze_incident_with_gemini(
    bundle: EvidenceBundle,
    create_interaction: InteractionCreator,
    model: str = DEFAULT_GEMINI_MODEL,
) -> AnalysisResponse:
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be a non-empty string")

    prompt = build_analysis_prompt(bundle)

    interaction = create_interaction(
        model=model,
        system_instruction=prompt.system_instructions,
        input=prompt.user_content,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ANALYSIS_RESPONSE_SCHEMA,
        },
        store=False,
    )

    raw_response = getattr(interaction, "output_text", None)
    if not isinstance(raw_response, str) or not raw_response.strip():
        raise ValueError(
            "Gemini returned an empty analysis response"
        )

    return parse_analysis_response(raw_response)