import json 
from datetime import datetime, timezone

#ข้อความ timestamp → parse_timestamp_utc() → เวลา UTC หรือ None → ลูปตัดสินใจว่าจะแสดงอะไร
def parse_timestamp_utc(timestamp_text: str) -> datetime | None: 
    timestamp = datetime.fromisoformat(timestamp_text)
    if timestamp.tzinfo is None:
        return None
    return timestamp.astimezone(timezone.utc)

if __name__ == "__main__":
    with open("sample.jsonl", "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                print(f"Invalid JSON on line {line_number}: {error}")
                continue
            timestamp_utc = parse_timestamp_utc(record["timestamp"])
            if timestamp_utc is None:
                print(f"Missing timezone on line {line_number}")
                continue
            print(
                f"{timestamp_utc.isoformat()} | "
                f"{record['service']} | {record['level']} | {record['message']}"
            )