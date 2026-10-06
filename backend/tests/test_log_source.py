import unittest
from datetime import datetime, timezone

from backend.app.ingestion.source import (
    RawLogEvent,
    collect_log_events,
)


class FakeLogSource:
    def __init__(self, events: list[RawLogEvent]):
        self.events = events
        self.requested_range = None

    def fetch_events(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> list[RawLogEvent]:
        self.requested_range = (start_time, end_time)
        return self.events


class TestCollectLogEvents(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime(
            2026,
            10,
            6,
            3,
            0,
            tzinfo=timezone.utc,
        )
        self.end_time = datetime(
            2026,
            10,
            6,
            3,
            5,
            tzinfo=timezone.utc,
        )
        self.event = RawLogEvent(
            source="cloudwatch",
            source_group="/aws/lambda/auth",
            source_stream="2026/10/06/auth-instance",
            source_id="event-123",
            timestamp=self.start_time,
            ingestion_time=self.start_time,
            message='{"service":"auth"}',
        )

    def test_collects_events_from_log_source(self):
        source = FakeLogSource([self.event])

        events = collect_log_events(
            source,
            self.start_time,
            self.end_time,
        )

        self.assertEqual(events, [self.event])
        self.assertEqual(
            source.requested_range,
            (self.start_time, self.end_time),
        )

    def test_rejects_timestamp_without_timezone(self):
        source = FakeLogSource([])
        naive_start = datetime(2026, 10, 6, 3, 0)

        with self.assertRaisesRegex(
            ValueError,
            "start_time must include timezone",
        ):
            collect_log_events(
                source,
                naive_start,
                self.end_time,
            )

    def test_rejects_invalid_time_range(self):
        source = FakeLogSource([])

        with self.assertRaisesRegex(
            ValueError,
            "end_time must be later than start_time",
        ):
            collect_log_events(
                source,
                self.end_time,
                self.start_time,
            )


if __name__ == "__main__":
    unittest.main()