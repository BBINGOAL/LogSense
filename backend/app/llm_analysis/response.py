import json
from dataclasses import dataclass


ANALYSIS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "observed_facts": {
            "type": "array",
            "items": {"type": "string"},
        },
        "likely_explanation": {"type": "string"},
        "uncertainty": {"type": "string"},
        "recommended_next_checks": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "observed_facts",
        "likely_explanation",
        "uncertainty",
        "recommended_next_checks",
    ],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class AnalysisResponse:
    observed_facts: tuple[str, ...]
    likely_explanation: str
    uncertainty: str
    recommended_next_checks: tuple[str, ...]


@dataclass(frozen=True)
class AnalysisMetadata:
    incident_id: str
    detector_name: str
    model: str
    prompt_version: str
    evidence_indices: tuple[int, ...]

    @property
    def evidence_count(self) -> int:
        return len(self.evidence_indices)


@dataclass(frozen=True)
class AnalysisResult:
    metadata: AnalysisMetadata
    response: AnalysisResponse


def _require_string(
    payload: dict[str, object],
    field_name: str,
) -> str:
    value = payload.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"{field_name} must be a non-empty string"
        )
    return value


def _require_string_list(
    payload: dict[str, object],
    field_name: str,
) -> tuple[str, ...]:
    value = payload.get(field_name)
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")

    if not all(
        isinstance(item, str) and item.strip()
        for item in value
    ):
        raise ValueError(
            f"{field_name} must contain only non-empty strings"
        )

    return tuple(value)


def parse_analysis_response(raw_response: str) -> AnalysisResponse:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise ValueError("LLM response is not valid JSON") from error

    if not isinstance(payload, dict):
        raise ValueError("LLM response must be a JSON object")

    expected_fields = set(ANALYSIS_RESPONSE_SCHEMA["required"])
    received_fields = set(payload)
    if received_fields != expected_fields:
        missing = sorted(expected_fields - received_fields)
        unexpected = sorted(received_fields - expected_fields)
        raise ValueError(
            "LLM response fields do not match schema: "
            f"missing={missing}, unexpected={unexpected}"
        )

    return AnalysisResponse(
        observed_facts=_require_string_list(
            payload,
            "observed_facts",
        ),
        likely_explanation=_require_string(
            payload,
            "likely_explanation",
        ),
        uncertainty=_require_string(payload, "uncertainty"),
        recommended_next_checks=_require_string_list(
            payload,
            "recommended_next_checks",
        ),
    )
