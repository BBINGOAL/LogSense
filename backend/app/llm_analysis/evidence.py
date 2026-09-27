import pandas as pd

from backend.app.incidents.models import Incident
from backend.app.llm_analysis.models import (
    EvidenceBundle,
    MetricEvidence,
)


REQUIRED_EVIDENCE_COLUMNS = (
    "window_start",
    "service",
    "request_count",
    "error_count",
    "error_rate",
    "mean_latency_ms",
    "p95_latency_ms",
    "anomaly_reason",
)


def _optional_float(
    value: object,
) -> float | None:
    if pd.isna(value):
        return None
    return float(value)


def _optional_text(
    value: object,
) -> str | None:
    if pd.isna(value):
        return None
    return str(value)


def build_evidence_bundle(
    incident: Incident,
    detections: pd.DataFrame,
    detector_name: str,
) -> EvidenceBundle:
    missing_columns = [
        column
        for column in REQUIRED_EVIDENCE_COLUMNS
        if column not in detections.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"missing evidence columns: {missing_text}"
        )

    missing_indices = [
        index
        for index in incident.evidence_indices
        if index not in detections.index
    ]

    if missing_indices:
        missing_text = ", ".join(
            str(index)
            for index in missing_indices
        )
        raise ValueError(
            f"missing evidence indices: {missing_text}"
        )

    metric_windows: list[MetricEvidence] = []

    for evidence_index in incident.evidence_indices:
        row = detections.loc[evidence_index]

        if str(row["service"]) != incident.service:
            raise ValueError(
                "evidence service must match incident service"
            )

        anomaly_score = None

        if "anomaly_score" in detections.columns:
            anomaly_score = _optional_float(
                row["anomaly_score"]
            )

        metric_windows.append(
            MetricEvidence(
                window_start=pd.to_datetime(
                    row["window_start"],
                    utc=True,
                ).to_pydatetime(),
                request_count=int(row["request_count"]),
                error_count=int(row["error_count"]),
                error_rate=float(row["error_rate"]),
                mean_latency_ms=_optional_float(
                    row["mean_latency_ms"]
                ),
                p95_latency_ms=_optional_float(
                    row["p95_latency_ms"]
                ),
                anomaly_reason=_optional_text(
                    row["anomaly_reason"]
                ),
                anomaly_score=anomaly_score,
            )
        )

    return EvidenceBundle(
        incident=incident,
        detector_name=detector_name,
        metric_windows=tuple(metric_windows),
    )