import unittest

import pandas as pd

from backend.app.detection.evaluation import (
    evaluate_predictions,
)
from backend.app.detection.ml_detector import (
    score_isolation_forest,
    train_isolation_forest,
)
from backend.app.detection.rules import apply_baseline_rules


class TestDetectorComparison(unittest.TestCase):
    def test_compares_detectors_on_labeled_synthetic_data(self):
        training_metrics = pd.DataFrame(
            {
                "request_count": [95, 100, 105, 98, 102] * 4,
                "error_rate": [0.01, 0.02, 0.00, 0.03, 0.01] * 4,
                "mean_latency_ms": [
                    90.0,
                    100.0,
                    110.0,
                    95.0,
                    105.0,
                ]
                * 4,
                "p95_latency_ms": [
                    140.0,
                    150.0,
                    160.0,
                    145.0,
                    155.0,
                ]
                * 4,
            }
        )

        labeled_metrics = pd.DataFrame(
            {
                "request_count": [100, 102, 98, 100, 100, 500],
                "error_rate": [
                    0.01,
                    0.02,
                    0.00,
                    0.80,
                    0.01,
                    0.90,
                ],
                "mean_latency_ms": [
                    100.0,
                    105.0,
                    95.0,
                    100.0,
                    800.0,
                    1500.0,
                ],
                "p95_latency_ms": [
                    150.0,
                    155.0,
                    145.0,
                    150.0,
                    1200.0,
                    2500.0,
                ],
                "actual_is_anomaly": [
                    False,
                    False,
                    False,
                    True,
                    True,
                    True,
                ],
            }
        )

        detector = train_isolation_forest(
            training_metrics,
            contamination=0.1,
        )

        ml_results = score_isolation_forest(
            detector,
            labeled_metrics,
        )
        rule_results = apply_baseline_rules(
            labeled_metrics,
        )

        actual = labeled_metrics["actual_is_anomaly"]

        ml_report = evaluate_predictions(
            actual,
            ml_results["ml_is_anomaly"],
        )
        rule_report = evaluate_predictions(
            actual,
            rule_results["is_anomaly"],
        )

        self.assertEqual(rule_report.precision, 1.0)
        self.assertEqual(rule_report.recall, 1.0)
        self.assertEqual(rule_report.f1_score, 1.0)
        self.assertEqual(rule_report.false_positives, 0)

        self.assertEqual(ml_report.precision, 1.0)
        self.assertAlmostEqual(ml_report.recall, 1 / 3)
        self.assertEqual(ml_report.f1_score, 0.5)
        self.assertEqual(ml_report.false_positives, 0)


if __name__ == "__main__":
    unittest.main()