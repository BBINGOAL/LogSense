import pandas as pd


MODEL_FEATURE_COLUMNS = (
    "request_count",
    "error_rate",
    "mean_latency_ms",
    "p95_latency_ms",
)


def select_model_features(
    metrics: pd.DataFrame,
) -> pd.DataFrame:
    missing_columns = [
        column
        for column in MODEL_FEATURE_COLUMNS
        if column not in metrics.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"missing model feature columns: {missing_text}"
        )

    return metrics.loc[
        :,
        list(MODEL_FEATURE_COLUMNS),
    ].copy()