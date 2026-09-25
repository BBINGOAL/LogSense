from backend.app.parsing.parser import LogParseError, parse_log_record


def main() -> None:
    with open("sample.jsonl", "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                record = parse_log_record(line)
            except LogParseError as error:
                print(f"Invalid log on line {line_number}: {error}")
                continue

            print(
                f"{record.timestamp.isoformat()} | "
                f"{record.service} | {record.level} | {record.message}"
            )


if __name__ == "__main__":
    main()