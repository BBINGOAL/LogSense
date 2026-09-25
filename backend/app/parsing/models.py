from dataclasses import dataclass
from datetime import datetime

@dataclass
class NormalizedLogRecord:
    timestamp: datetime
    service: str
    level: str
    message: str
    request_id: str | None = None
    status_code: int | None = None
    latency_ms: float | None = None