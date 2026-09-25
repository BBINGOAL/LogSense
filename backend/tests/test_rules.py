import unittest

import pandas as pd

from backend.app.detection.rules import apply_error_rate_rule


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


if __name__ == "__main__":
    unittest.main()