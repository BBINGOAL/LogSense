import unittest

import pandas as pd

from backend.app.metrics.filters import filter_by_level


class TestFilterByLevel(unittest.TestCase):
    def test_returns_only_matching_log_levels(self):
        frame = pd.DataFrame(
            {
                "level": ["ERROR", "INFO", "ERROR"],
                "message": ["failed", "started", "timeout"],
            }
        )

        result = filter_by_level(frame, "error")

        self.assertEqual(result["level"].tolist(), ["ERROR", "ERROR"])
        self.assertEqual(
            result["message"].tolist(),
            ["failed", "timeout"],
        )
        self.assertEqual(result.index.tolist(), [0, 1])


if __name__ == "__main__":
    unittest.main()