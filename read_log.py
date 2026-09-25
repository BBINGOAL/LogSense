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

    print("\nWindow metrics:")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()