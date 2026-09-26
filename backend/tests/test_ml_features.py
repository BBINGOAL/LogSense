import unittest

import pandas as pd

from backend.app.detection.ml_features import (
    MODEL_FEATURE_COLUMNS,
    select_model_features,
)


class TestSelectModelFeatures(unittest.TestCase):
    def test_selects_only_model_features(self):
        metrics = pd.DataFrame(
            {
                "window_start": [
                    "2026-09-26T10:00:00Z",
                    "2026-09-26T10:05:00Z",
                ],
                "service": ["auth", "auth"],
                "request_count": [10, 20],
                "error_count": [1, 4],
                "error_rate": [0.1, 0.2],
                "mean_latency_ms": [100.0, None],
                "p95_latency_ms": [180.0, None],
            }
        )

        features = select_model_features(metrics)

        self.assertEqual(
            list(features.columns),
            list(MODEL_FEATURE_COLUMNS),
        )
        self.assertEqual(features.shape, (2, 4))
        self.assertTrue(
            pd.isna(features.loc[1, "p95_latency_ms"])
        )

    def test_rejects_missing_feature_columns(self):
        metrics = pd.DataFrame(
            {
                "request_count": [10],
            }
        )

        with self.assertRaisesRegex(
            ValueError,
            "error_rate",
        ):
            select_model_features(metrics)


if __name__ == "__main__":
    unittest.main()