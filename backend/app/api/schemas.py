from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class DashboardIncident(BaseModel):
    incident_id: str
    service: str
    started_at: datetime
    ended_at: datetime
    severity: Literal["low", "medium", "high"]
    triggers: list[str]
    evidence_indices: list[int]
    status: Literal["open", "resolved"]


class DashboardMetricWindow(BaseModel):
    window_start: datetime
    request_count: int
    error_count: int
    error_rate: float
    mean_latency_ms: float | None
    p95_latency_ms: float | None
    anomaly_reason: str | None
    anomaly_score: float | None = None


class DashboardAnalysisMetadata(BaseModel):
    incident_id: str
    detector_name: str
    model: str
    prompt_version: str
    evidence_indices: list[int]


class DashboardAnalysisResponse(BaseModel):
    observed_facts: list[str]
    likely_explanation: str
    uncertainty: str
    recommended_next_checks: list[str]


class DashboardAnalysis(BaseModel):
    metadata: DashboardAnalysisMetadata
    response: DashboardAnalysisResponse


class DashboardIncidentRecord(BaseModel):
    incident: DashboardIncident
    metric_windows: list[DashboardMetricWindow]
    analysis: DashboardAnalysis
