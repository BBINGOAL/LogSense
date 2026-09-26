import unittest

import pandas as pd

from backend.app.detection.ml_detector import (
    score_isolation_forest,
    train_isolation_forest,
)
from backend.app.detection.ml_features import (
    MODEL_FEATURE_COLUMNS,
    select_model_features,
)


class TestTrainIsolationForest(unittest.TestCase):
    def test_trains_pipeline_and_imputes_missing_latency(self):
        metrics = pd.DataFrame(
            {
                "request_count": [10, 12, 11],
                "error_rate": [0.01, 0.02, 0.01],
                "mean_latency_ms": [100.0, None, 300.0],
                "p95_latency_ms": [150.0, None, 450.0],
            }
        )

        detector = train_isolation_forest(metrics)
        features = select_model_features(metrics)
        transformed = detector.named_steps[
            "imputer"
        ].transform(features)

        self.assertFalse(pd.isna(transformed).any())
        self.assertEqual(transformed[1, 2], 200.0)
        self.assertEqual(transformed[1, 3], 300.0)
        self.assertTrue(
            hasattr(
                detector.named_steps["model"],
                "estimators_",
            )
        )

    def test_rejects_empty_training_metrics(self):
        metrics = pd.DataFrame(
            columns=MODEL_FEATURE_COLUMNS,
        )

        with self.assertRaisesRegex(
            ValueError,
            "empty metrics",
        ):
            train_isolation_forest(metrics)

    def test_rejects_invalid_contamination(self):
        metrics = pd.DataFrame(
            {
                "request_count": [10],
                "error_rate": [0.01],
                "mean_latency_ms": [100.0],
                "p95_latency_ms": [150.0],
            }
        )

        with self.assertRaisesRegex(
            ValueError,
            "contamination",
        ):
            train_isolation_forest(
                metrics,
                contamination=0.0,
            )


class TestScoreIsolationForest(unittest.TestCase):
    def test_marks_obvious_outlier_as_anomaly(self):
        normal_count = 10
        metrics = pd.DataFrame(
            {
                "request_count": [100] * normal_count + [500],
                "error_rate": [0.01] * normal_count + [0.90],
                "mean_latency_ms": (
                    [100.0] * normal_count + [3000.0]
                ),
                "p95_latency_ms": (
                    [150.0] * normal_count + [5000.0]
                ),
            }
        )

        detector = train_isolation_forest(
            metrics,
            contamination=0.1,
        )
        result = score_isolation_forest(
            detector,
            metrics,
        )

        outlier_index = len(metrics) - 1

        self.assertTrue(
            result.loc[outlier_index, "ml_is_anomaly"]
        )
        self.assertGreater(
            result.loc[outlier_index, "anomaly_score"],
            result.loc[0, "anomaly_score"],
        )

    def test_returns_empty_scoring_schema(self):
        training_metrics = pd.DataFrame(
            {
                "request_count": [100],
                "error_rate": [0.01],
                "mean_latency_ms": [100.0],
                "p95_latency_ms": [150.0],
            }
        )
        detector = train_isolation_forest(training_metrics)
        empty_metrics = pd.DataFrame(
            columns=MODEL_FEATURE_COLUMNS,
        )

        result = score_isolation_forest(
            detector,
            empty_metrics,
        )

        self.assertTrue(result.empty)
        self.assertIn("anomaly_score", result.columns)
        self.assertIn("ml_is_anomaly", result.columns)


if __name__ == "__main__":
    unittest.main()
