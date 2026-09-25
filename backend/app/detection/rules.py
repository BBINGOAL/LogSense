import pandas as pd


def apply_error_rate_rule(
    metrics: pd.DataFrame,
    threshold: float = 0.5,
) -> pd.DataFrame:
    result = metrics.copy()
    result["is_anomaly"] = result["error_rate"] >= threshold
    return result


def apply_latency_rule(
    metrics: pd.DataFrame,
    threshold_ms: float = 500.0,
) -> pd.DataFrame:
    result = metrics.copy()
    result["is_anomaly"] = (
        result["p95_latency_ms"]
        .ge(threshold_ms)
        .fillna(False)
    )
    return result