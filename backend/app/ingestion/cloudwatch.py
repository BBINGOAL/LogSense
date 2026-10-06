from datetime import datetime, timezone
from typing import Any, Protocol
from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
)

from backend.app.ingestion.source import RawLogEvent


class CloudWatchLogSourceError(RuntimeError):
    """CloudWatch could not provide log events."""


class CloudWatchLogsClient(Protocol):
    def filter_log_events(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        ...


def _to_epoch_milliseconds(timestamp: datetime) -> int:
    return int(timestamp.timestamp() * 1000)


def _from_epoch_milliseconds(value: int) -> datetime:
    return datetime.fromtimestamp(
        value / 1000,
        tz=timezone.utc,
    )


class CloudWatchLogSource:
    def __init__(
        self,
        client: CloudWatchLogsClient,
        log_group_name: str,
    ):
        if not log_group_name.strip():
            raise ValueError("log_group_name must not be empty")

        self.client = client
        self.log_group_name = log_group_name

    def fetch_events(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> list[RawLogEvent]:
        request: dict[str, Any] = {
            "logGroupName": self.log_group_name,
            "startTime": _to_epoch_milliseconds(start_time),
            "endTime": _to_epoch_milliseconds(end_time),
            "startFromHead": True,
        }

        raw_events = []

        while True:
            try:
                response = self.client.filter_log_events(**request)
            except NoCredentialsError as error:
                raise CloudWatchLogSourceError(
                    "CloudWatch credentials are not configured"
                ) from error
            except EndpointConnectionError as error:
                raise CloudWatchLogSourceError(
                    "Could not connect to CloudWatch Logs"
                ) from error
            except ClientError as error:
                error_code = error.response.get(
                    "Error",
                    {},
                ).get(
                    "Code",
                    "Unknown",
                )

                raise CloudWatchLogSourceError(
                    "CloudWatch rejected FilterLogEvents "
                    f"({error_code})"
                ) from error

            for event in response.get("events", []):
                ingestion_time_ms = event.get("ingestionTime")

                raw_events.append(
                    RawLogEvent(
                        source="cloudwatch",
                        source_group=self.log_group_name,
                        source_stream=event["logStreamName"],
                        source_id=event["eventId"],
                        timestamp=_from_epoch_milliseconds(
                            event["timestamp"]
                        ),
                        ingestion_time=(
                            None
                            if ingestion_time_ms is None
                            else _from_epoch_milliseconds(
                                ingestion_time_ms
                            )
                        ),
                        message=event["message"],
                    )
                )

            next_token = response.get("nextToken")

            if next_token is None:
                break

            request["nextToken"] = next_token

        return raw_events
