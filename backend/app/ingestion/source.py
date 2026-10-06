from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class RawLogEvent:
    source: str
    source_group: str
    source_stream: str
    source_id: str
    timestamp: datetime
    ingestion_time: datetime | None
    message: str


class LogSource(Protocol):
    def fetch_events(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> list[RawLogEvent]:
        ...


def _require_timezone(
    timestamp: datetime,
    field_name: str,
) -> None:
    if timestamp.tzinfo is None:
        raise ValueError(
            f"{field_name} must include timezone"
        )


def collect_log_events(
    source: LogSource,
    start_time: datetime,
    end_time: datetime,
) -> list[RawLogEvent]:
    _require_timezone(start_time, "start_time")
    _require_timezone(end_time, "end_time")

    if end_time <= start_time:
        raise ValueError(
            "end_time must be later than start_time"
        )

    return source.fetch_events(start_time, end_time)