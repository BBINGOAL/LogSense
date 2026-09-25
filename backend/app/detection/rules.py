import pandas as pd


def apply_error_rate_rule(
    metrics: pd.DataFrame,
    threshold: float = 0.5,
) -> pd.DataFrame:
    result = metrics.copy()
    result["is_anomaly"] = result["error_rate"] >= threshold
    return result