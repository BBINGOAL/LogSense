from dataclasses import dataclass
from datetime import datetime

from backend.app.incidents.models import Incident


@dataclass(frozen=True)
class MetricEvidence:
    window_start: datetime
    request_count: int
    error_count: int
    error_rate: float
    mean_latency_ms: float | None
    p95_latency_ms: float | None
    anomaly_reason: str | None
    anomaly_score: float | None = None


@dataclass(frozen=True)
class EvidenceBundle:
    incident: Incident
    detector_name: str
    metric_windows: tuple[MetricEvidence, ...]
    log_samples: tuple[str, ...] = ()

    @property
    def metric_window_count(self) -> int:
        return len(self.metric_windows)