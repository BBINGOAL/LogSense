import unittest

import pandas as pd

from backend.app.detection.rules import (
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
        
        
if __name__ == "__main__":
    unittest.main()