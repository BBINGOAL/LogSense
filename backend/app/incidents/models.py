from dataclasses import dataclass
from datetime import datetime
from typing import Literal


IncidentSeverity = Literal["low", "medium", "high"]
IncidentStatus = Literal["open", "resolved"]


@dataclass(frozen=True)
class Incident:
    incident_id: str
    service: str
    started_at: datetime
    ended_at: datetime
    severity: IncidentSeverity
    triggers: tuple[str, ...]
    evidence_indices: tuple[int, ...]
    status: IncidentStatus = "open"

    @property
    def anomaly_count(self) -> int:
        return len(self.evidence_indices)