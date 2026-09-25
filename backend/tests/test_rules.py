import unittest

import pandas as pd

from backend.app.detection.rules import (
    apply_baseline_rules,
    apply_error_rate_rule,
    apply_latency_rule,
)


class TestApplyErrorRateRule(unittest.TestCase):
    def test_marks_rates_at_or_above_threshold_as_anomalies(self):
        metrics = pd.DataFrame(
            {
                "error_rate": [0.49, 0.50, 0.80],
            }
        )

        result = apply_error_rate_rule(
            metrics,
            threshold=0.50,
        )

        self.assertEqual(
            result["is_anomaly"].tolist(),
            [False, True, True],
        )

    def test_rejects_error_rate_threshold_above_one(self):
        metrics = pd.DataFrame(
            {
                "error_rate": [0.5],
            }
        )

        with self.assertRaisesRegex(
            ValueError,
            "between 0.0 and 1.0",
        ):
            apply_error_rate_rule(
                metrics,
                threshold=1.1,
            )


class TestApplyLatencyRule(unittest.TestCase):
    def test_marks_high_latency_as_anomaly(self):
        metrics = pd.DataFrame(
            {
                "p95_latency_ms": [
                    499.0,
                    500.0,
                    900.0,
                    None,
                ],
            }
        )

        result = apply_latency_rule(
            metrics,
            threshold_ms=500.0,
        )

        self.assertEqual(
            result["is_anomaly"].tolist(),
            [False, True, True, False],
        )

    def test_rejects_negative_latency_threshold(self):
        metrics = pd.DataFrame(
            {
                "p95_latency_ms": [100.0],
            }
        )

        with self.assertRaisesRegex(
            ValueError,
            "non-negative",
        ):
            apply_latency_rule(
                metrics,
                threshold_ms=-1.0,
            )


class TestApplyBaselineRules(unittest.TestCase):
    def test_combines_rule_results_and_reasons(self):
        metrics = pd.DataFrame(
            {
                "error_rate": [0.1, 0.6, 0.1, 0.6],
                "p95_latency_ms": [
                    100.0,
                    100.0,
                    600.0,
                    600.0,
                ],
            }
        )

        result = apply_baseline_rules(metrics)

        self.assertEqual(
            result["is_anomaly"].tolist(),
            [False, True, True, True],
        )
        self.assertEqual(
            result["anomaly_reason"]
            .fillna("none")
            .tolist(),
            [
                "none",
                "high_error_rate",
                "high_latency",
                "high_error_rate,high_latency",
            ],
        )

    def test_handles_empty_metrics(self):
        metrics = pd.DataFrame(
            {
                "error_rate": pd.Series(dtype="Float64"),
                "p95_latency_ms": pd.Series(dtype="Float64"),
            }
        )

        result = apply_baseline_rules(metrics)

        self.assertTrue(result.empty)
        self.assertIn("is_anomaly", result.columns)
        self.assertIn("anomaly_reason", result.columns)


if __name__ == "__main__":
    unittest.main()
