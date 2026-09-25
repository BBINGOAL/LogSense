import pandas as pd


def build_window_metrics(
    frame: pd.DataFrame,
    window: str = "5min",
) -> pd.DataFrame:
    working_frame = frame.assign(
        is_error=frame["level"].eq("ERROR")
    )

    metrics = (
        working_frame.set_index("timestamp")
        .groupby("service")
        .resample(window)
        .agg(
            request_count=("level", "size"),
            error_count=("is_error", "sum"),
            mean_latency_ms=("latency_ms", "mean"),
            p95_latency_ms=(
                "latency_ms",
                lambda values: values.quantile(0.95),
            ),
        )
        .reset_index()
        .rename(columns={"timestamp": "window_start"})
    )

    metrics["error_rate"] = (
        metrics["error_count"] / metrics["request_count"]
    )

    return metrics[
        [
            "window_start",
            "service",
            "request_count",
            "error_count",
            "error_rate",
            "mean_latency_ms",
            "p95_latency_ms",
        ]
    ]