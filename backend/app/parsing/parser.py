import json
from datetime import datetime, timezone

from .models import NormalizedLogRecord

#return เป็น class ที่ normalize เเล้ว  
def parse_log_record(raw_line: str) -> NormalizedLogRecord:
    data = json.loads(raw_line)

    timestamp = datetime.fromisoformat(data["timestamp"])
    if timestamp.tzinfo is None:
        raise ValueError("timestamp must include timezone")

    return NormalizedLogRecord(
        timestamp=timestamp.astimezone(timezone.utc),
        service=data["service"],
        level=data["level"].upper(),
        message=data["message"],
        request_id=data.get("request_id"),
        status_code=data.get("status_code"),
        latency_ms=data.get("latency_ms"),
    )