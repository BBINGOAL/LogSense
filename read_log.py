from backend.app.detection.rules import apply_baseline_rules
from backend.app.incidents.grouping import (
    group_anomalies_into_incidents,
)
from backend.app.metrics.dataframe import records_to_dataframe
from backend.app.metrics.features import build_window_metrics
from backend.app.parsing.models import NormalizedLogRecord
from backend.app.parsing.parser import LogParseError, parse_log_record


def main() -> None:
    records: list[NormalizedLogRecord] = []

    with open("sample.jsonl", "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                record = parse_log_record(line)
            except LogParseError as error:
                print(f"Invalid log on line {line_number}: {error}")
                continue

            records.append(record)

    frame = records_to_dataframe(records)
    metrics = build_window_metrics(frame)
    detection_results = apply_baseline_rules(metrics)
    incidents = group_anomalies_into_incidents(detection_results)

    print("\nWindow metrics:")
    print(metrics.to_string(index=False))
    print("\nRule-based detection:")
    print(
        detection_results[
            [
                "window_start",
                "service",
                "error_rate",
                "p95_latency_ms",
                "is_anomaly",
                "anomaly_reason",
            ]
        ].to_string(index=False)
    )
    print("\nIncidents:")

    if not incidents:
        print("No incidents detected.")
    else:
        for incident in incidents:
            triggers = ",".join(incident.triggers)

            print(
                f"{incident.incident_id} | "
                f"service={incident.service} | "
                f"severity={incident.severity} | "
                f"status={incident.status} | "
                f"period={incident.started_at.isoformat()}"
                f" -> {incident.ended_at.isoformat()} | "
                f"anomalies={incident.anomaly_count} | "
                f"triggers={triggers}"
            )


if __name__ == "__main__":
    main()