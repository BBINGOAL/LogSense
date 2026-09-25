from dataclasses import asdict

import pandas as pd

from backend.app.parsing.models import NormalizedLogRecord


LOG_COLUMNS = (
    "timestamp",
    "service",
    "level",
    "message",
    "request_id",
    "status_code",
    "latency_ms",
)


def records_to_dataframe(
    records: list[NormalizedLogRecord],
) -> pd.DataFrame:
    rows = [asdict(record) for record in records]
    frame = pd.DataFrame(rows, columns=LOG_COLUMNS)

    frame["timestamp"] = pd.to_datetime(
        frame["timestamp"],
        utc=True,
    )

    return frame.astype(
        {
            "service": "string",
            "level": "string",
            "message": "string",
            "request_id": "string",
            "status_code": "Int64",
            "latency_ms": "Float64",
        }
    )