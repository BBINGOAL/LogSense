import os

import boto3
from dotenv import load_dotenv

from backend.app.ingestion.cloudwatch import (
    CloudWatchLogSource,
)


def create_cloudwatch_log_source() -> CloudWatchLogSource:
    load_dotenv()

    region_name = os.getenv("AWS_REGION", "").strip()
    log_group_name = os.getenv(
        "AWS_LOG_GROUP_NAME",
        "",
    ).strip()

    if not region_name:
        raise RuntimeError("AWS_REGION is not configured")

    if not log_group_name:
        raise RuntimeError(
            "AWS_LOG_GROUP_NAME is not configured"
        )

    client = boto3.client(
        "logs",
        region_name=region_name,
    )

    return CloudWatchLogSource(
        client=client,
        log_group_name=log_group_name,
    )