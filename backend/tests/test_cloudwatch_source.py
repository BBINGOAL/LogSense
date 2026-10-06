import unittest
from datetime import datetime, timedelta, timezone
from typing import Any

from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
)

from backend.app.ingestion.cloudwatch import (
    CloudWatchLogSource,
    CloudWatchLogSourceError,
)
from backend.app.ingestion.source import (
    RawLogEvent,
    collect_log_events,
)


class FakeCloudWatchLogsClient:
    def __init__(self, response: dict[str, Any]):
        self.response = response
        self.request: dict[str, Any] | None = None

    def filter_log_events(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        self.request = kwargs
        return self.response


class PagedFakeCloudWatchLogsClient:
    def __init__(
        self,
        responses: list[dict[str, Any]],
    ):
        self.responses = responses
        self.requests: list[dict[str, Any]] = []

    def filter_log_events(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        response_index = len(self.requests)
        self.requests.append(kwargs)
        return self.responses[response_index]


class FailingCloudWatchLogsClient:
    def __init__(self, error: Exception):
        self.error = error

    def filter_log_events(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        raise self.error


class TestCloudWatchLogSource(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime(
            2026,
            10,
            6,
            3,
            0,
            tzinfo=timezone.utc,
        )
        self.end_time = self.start_time + timedelta(minutes=5)
        self.ingestion_time = self.start_time + timedelta(seconds=1)

    def test_fetches_and_maps_cloudwatch_events(self):
        client = FakeCloudWatchLogsClient(
            {
                "events": [
                    {
                        "eventId": "event-123",
                        "logStreamName": "auth-stream",
                        "timestamp": int(
                            self.start_time.timestamp() * 1000
                        ),
                        "ingestionTime": int(
                            self.ingestion_time.timestamp() * 1000
                        ),
                        "message": '{"service":"auth"}',
                    }
                ]
            }
        )
        source = CloudWatchLogSource(
            client=client,
            log_group_name="/aws/lambda/auth",
        )

        events = collect_log_events(
            source,
            self.start_time,
            self.end_time,
        )

        self.assertEqual(
            client.request,
            {
                "logGroupName": "/aws/lambda/auth",
                "startTime": int(
                    self.start_time.timestamp() * 1000
                ),
                "endTime": int(
                    self.end_time.timestamp() * 1000
                ),
                "startFromHead": True,
            },
        )
        self.assertEqual(
            events,
            [
                RawLogEvent(
                    source="cloudwatch",
                    source_group="/aws/lambda/auth",
                    source_stream="auth-stream",
                    source_id="event-123",
                    timestamp=self.start_time,
                    ingestion_time=self.ingestion_time,
                    message='{"service":"auth"}',
                )
            ],
        )

    def test_returns_empty_list_when_no_events_exist(self):
        client = FakeCloudWatchLogsClient({})
        source = CloudWatchLogSource(
            client=client,
            log_group_name="/aws/lambda/auth",
        )

        events = collect_log_events(
            source,
            self.start_time,
            self.end_time,
        )

        self.assertEqual(events, [])

    def test_maps_missing_ingestion_time_to_none(self):
        client = FakeCloudWatchLogsClient(
            {
                "events": [
                    {
                        "eventId": "event-456",
                        "logStreamName": "auth-stream",
                        "timestamp": int(
                            self.start_time.timestamp() * 1000
                        ),
                        "message": '{"service":"auth"}',
                    }
                ]
            }
        )
        source = CloudWatchLogSource(
            client=client,
            log_group_name="/aws/lambda/auth",
        )

        events = collect_log_events(
            source,
            self.start_time,
            self.end_time,
        )

        self.assertIsNone(events[0].ingestion_time)

    def test_rejects_empty_log_group_name(self):
        client = FakeCloudWatchLogsClient({})

        with self.assertRaisesRegex(
            ValueError,
            "log_group_name must not be empty",
        ):
            CloudWatchLogSource(
                client=client,
                log_group_name=" ",
            )

    def test_fetches_all_pages_including_after_empty_page(self):
        second_timestamp = self.start_time + timedelta(seconds=10)

        client = PagedFakeCloudWatchLogsClient(
            [
                {
                    "events": [
                        {
                            "eventId": "event-1",
                            "logStreamName": "auth-stream",
                            "timestamp": int(
                                self.start_time.timestamp() * 1000
                            ),
                            "message": '{"sequence":1}',
                        }
                    ],
                    "nextToken": "page-2",
                },
                {
                    "events": [],
                    "nextToken": "page-3",
                },
                {
                    "events": [
                        {
                            "eventId": "event-2",
                            "logStreamName": "auth-stream",
                            "timestamp": int(
                                second_timestamp.timestamp() * 1000
                            ),
                            "message": '{"sequence":2}',
                        }
                    ]
                },
            ]
        )
        source = CloudWatchLogSource(
            client=client,
            log_group_name="/aws/lambda/auth",
        )

        events = collect_log_events(
            source,
            self.start_time,
            self.end_time,
        )

        self.assertEqual(
            [event.source_id for event in events],
            ["event-1", "event-2"],
        )
        self.assertEqual(len(client.requests), 3)
        self.assertNotIn("nextToken", client.requests[0])
        self.assertEqual(
            client.requests[1]["nextToken"],
            "page-2",
        )
        self.assertEqual(
            client.requests[2]["nextToken"],
            "page-3",
        )

    def test_reports_missing_credentials(self):
        original_error = NoCredentialsError()
        client = FailingCloudWatchLogsClient(original_error)
        source = CloudWatchLogSource(
            client=client,
            log_group_name="/aws/lambda/auth",
        )

        with self.assertRaisesRegex(
            CloudWatchLogSourceError,
            "credentials are not configured",
        ) as context:
            collect_log_events(
                source,
                self.start_time,
                self.end_time,
            )

        self.assertIs(
            context.exception.__cause__,
            original_error,
        )

    def test_reports_connection_failure(self):
        original_error = EndpointConnectionError(
            endpoint_url="https://logs.example"
        )
        client = FailingCloudWatchLogsClient(original_error)
        source = CloudWatchLogSource(
            client=client,
            log_group_name="/aws/lambda/auth",
        )

        with self.assertRaisesRegex(
            CloudWatchLogSourceError,
            "Could not connect to CloudWatch Logs",
        ):
            collect_log_events(
                source,
                self.start_time,
                self.end_time,
            )

    def test_reports_aws_permission_error_code(self):
        original_error = ClientError(
            {
                "Error": {
                    "Code": "AccessDeniedException",
                    "Message": "Access denied",
                }
            },
            "FilterLogEvents",
        )
        client = FailingCloudWatchLogsClient(original_error)
        source = CloudWatchLogSource(
            client=client,
            log_group_name="/aws/lambda/auth",
        )

        with self.assertRaisesRegex(
            CloudWatchLogSourceError,
            "AccessDeniedException",
        ):
            collect_log_events(
                source,
                self.start_time,
                self.end_time,
            )


if __name__ == "__main__":
    unittest.main()
