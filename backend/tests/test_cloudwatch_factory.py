import os
import unittest
from unittest.mock import patch

from backend.app.ingestion.cloudwatch_factory import (
    create_cloudwatch_log_source,
)


class TestCreateCloudWatchLogSource(unittest.TestCase):
    def test_creates_source_from_environment(self):
        fake_client = object()

        with (
            patch.dict(
                os.environ,
                {
                    "AWS_REGION": "ap-southeast-1",
                    "AWS_LOG_GROUP_NAME": "/aws/lambda/auth",
                },
                clear=True,
            ),
            patch(
                "backend.app.ingestion."
                "cloudwatch_factory.load_dotenv"
            ),
            patch(
                "backend.app.ingestion."
                "cloudwatch_factory.boto3.client",
                return_value=fake_client,
            ) as client_factory,
        ):
            source = create_cloudwatch_log_source()

        client_factory.assert_called_once_with(
            "logs",
            region_name="ap-southeast-1",
        )
        self.assertIs(source.client, fake_client)
        self.assertEqual(
            source.log_group_name,
            "/aws/lambda/auth",
        )

    def test_rejects_missing_region(self):
        with (
            patch.dict(
                os.environ,
                {
                    "AWS_LOG_GROUP_NAME": "/aws/lambda/auth",
                },
                clear=True,
            ),
            patch(
                "backend.app.ingestion."
                "cloudwatch_factory.load_dotenv"
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "AWS_REGION is not configured",
            ):
                create_cloudwatch_log_source()

    def test_rejects_missing_log_group(self):
        with (
            patch.dict(
                os.environ,
                {
                    "AWS_REGION": "ap-southeast-1",
                },
                clear=True,
            ),
            patch(
                "backend.app.ingestion."
                "cloudwatch_factory.load_dotenv"
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "AWS_LOG_GROUP_NAME is not configured",
            ):
                create_cloudwatch_log_source()


if __name__ == "__main__":
    unittest.main()