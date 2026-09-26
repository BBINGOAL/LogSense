from datetime import timedelta

import pandas as pd

from backend.app.incidents.models import (
    Incident,
    IncidentSeverity,
)

REQUIRED_DETECTION_COLUMNS = (
    "window_start",
    "service",
    "is_anomaly",
    "anomaly_reason",
)


def _severity_for_count(
    anomaly_count: int,
) -> IncidentSeverity:
    if anomaly_count >= 3:
        return "high"
    if anomaly_count == 2:
        return "medium"
    return "low"


def _build_incident(
    group: pd.DataFrame,
) -> Incident:
    started_at = group["window_start"].iloc[0].to_pydatetime()
    ended_at = group["window_start"].iloc[-1].to_pydatetime()
    service = str(group["service"].iloc[0])

    trigger_set: set[str] = set()

    for reason in group["anomaly_reason"].dropna():
        trigger_set.update(
            trigger.strip()
            for trigger in str(reason).split(",")
            if trigger.strip()
        )

    return Incident(
        incident_id=(
            f"{service}-"
            f"{started_at.strftime('%Y%m%dT%H%M%SZ')}"
        ),
        service=service,
        started_at=started_at,
        ended_at=ended_at,
        severity=_severity_for_count(len(group)),
        triggers=tuple(sorted(trigger_set)),
        evidence_indices=tuple(
            int(index)
            for index in group.index
        ),
    )


def group_anomalies_into_incidents(
    detections: pd.DataFrame,
    max_gap: timedelta = timedelta(minutes=10),
) -> list[Incident]:
    missing_columns = [
        column
        for column in REQUIRED_DETECTION_COLUMNS
        if column not in detections.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"missing detection columns: {missing_text}"
        )

    if max_gap <= timedelta(0):
        raise ValueError(
            "max_gap must be greater than zero"
        )

    anomalies = detections.loc[
        detections["is_anomaly"].fillna(False)
    ].copy()

    if anomalies.empty:
        return []

    try:
        anomalies["window_start"] = pd.to_datetime(
            anomalies["window_start"],
            utc=True,
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "anomaly window_start must contain valid timestamps"
        ) from error

    anomalies = anomalies.sort_values(
        ["service", "window_start"]
    )

    service_changed = (
        anomalies["service"]
        .ne(anomalies["service"].shift())
        .fillna(True)
    )
    time_gap = (
        anomalies["window_start"]
        - anomalies["window_start"].shift()
    )
    gap_exceeded = time_gap.gt(max_gap).fillna(False)

    anomalies["_incident_group"] = (
        service_changed | gap_exceeded
    ).cumsum()

    return [
        _build_incident(group)
        for _, group in anomalies.groupby(
            "_incident_group",
            sort=False,
        )
    ]
