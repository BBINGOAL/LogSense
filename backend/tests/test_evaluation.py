import unittest

from backend.app.detection.evaluation import (
    evaluate_predictions,
)


class TestEvaluatePredictions(unittest.TestCase):
    def test_calculates_classification_metrics(self):
        actual = [False, False, True, True, True]
        predicted = [False, True, True, False, True]

        report = evaluate_predictions(actual, predicted)

        self.assertAlmostEqual(report.precision, 2 / 3)
        self.assertAlmostEqual(report.recall, 2 / 3)
        self.assertAlmostEqual(report.f1_score, 2 / 3)
        self.assertEqual(report.true_positives, 2)
        self.assertEqual(report.false_positives, 1)
        self.assertEqual(report.false_negatives, 1)
        self.assertEqual(report.true_negatives, 1)

    def test_returns_zero_when_no_anomaly_is_predicted(self):
        actual = [False, True]
        predicted = [False, False]

        report = evaluate_predictions(actual, predicted)

        self.assertEqual(report.precision, 0.0)
        self.assertEqual(report.recall, 0.0)
        self.assertEqual(report.f1_score, 0.0)
        self.assertEqual(report.false_positives, 0)
        self.assertEqual(report.false_negatives, 1)

    def test_rejects_different_label_lengths(self):
        with self.assertRaisesRegex(
            ValueError,
            "equal length",
        ):
            evaluate_predictions(
                actual=[False, True],
                predicted=[False],
            )


if __name__ == "__main__":
    unittest.main()