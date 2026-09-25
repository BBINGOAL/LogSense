import json
from datetime import datetime, timezone
from .models import NormalizedLogRecord

REQUIRED_FIELDS = ("timestamp", "service", "level", "message")

class LogParseError(ValueError):
    pass

def parse_log_record(raw_line: str) -> NormalizedLogRecord:
    try:
        data = json.loads(raw_line)
    except json.JSONDecodeError as error:
        raise LogParseError(f"invalid JSON: {error.msg}") from error

    for field in REQUIRED_FIELDS:
        if field not in data:
            raise LogParseError(f"missing required field: {field}")
    try:
        timestamp = datetime.fromisoformat(data["timestamp"])
    except (TypeError, ValueError) as error:
        raise LogParseError("invalid timestamp") from error

    if timestamp.tzinfo is None:
        raise LogParseError("timestamp must include timezone")

    return NormalizedLogRecord(
        timestamp=timestamp.astimezone(timezone.utc),
        service=data["service"],
        level=data["level"].upper(),
        message=data["message"],
        request_id=data.get("request_id"),
        status_code=data.get("status_code"),
        latency_ms=data.get("latency_ms"),
    )