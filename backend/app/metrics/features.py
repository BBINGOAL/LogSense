import pandas as pd


def build_request_count_metrics(
    frame: pd.DataFrame,
    window: str = "5min",
) -> pd.DataFrame:
    metrics = (
        frame.set_index("timestamp")
        .groupby("service")
        .resample(window)
        .size()
        .rename("request_count")
        .reset_index()
        .rename(columns={"timestamp": "window_start"})
    )

    return metrics[
        ["window_start", "service", "request_count"]
    ]