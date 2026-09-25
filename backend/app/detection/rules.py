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


def apply_baseline_rules(
    metrics: pd.DataFrame,
    error_rate_threshold: float = 0.5,
    latency_threshold_ms: float = 500.0,
) -> pd.DataFrame:
    result = metrics.copy()

    error_result = apply_error_rate_rule(
        metrics,
        threshold=error_rate_threshold,
    )
    latency_result = apply_latency_rule(
        metrics,
        threshold_ms=latency_threshold_ms,
    )

    result["error_rate_anomaly"] = error_result["is_anomaly"]
    result["latency_anomaly"] = latency_result["is_anomaly"]

    result["is_anomaly"] = (
        result["error_rate_anomaly"]
        | result["latency_anomaly"]
    )

    result["anomaly_reason"] = pd.Series(
        pd.NA,
        index=result.index,
        dtype="string",
    )

    result.loc[
        result["error_rate_anomaly"],
        "anomaly_reason",
    ] = "high_error_rate"

    result.loc[
        result["latency_anomaly"],
        "anomaly_reason",
    ] = "high_latency"

    both_rules = (
        result["error_rate_anomaly"]
        & result["latency_anomaly"]
    )
    result.loc[
        both_rules,
        "anomaly_reason",
    ] = "high_error_rate,high_latency"

    return result