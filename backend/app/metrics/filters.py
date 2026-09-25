import pandas as pd


def filter_by_level(
    frame: pd.DataFrame,
    level: str,
) -> pd.DataFrame:
    normalized_level = level.upper()
    matching_rows = frame["level"] == normalized_level

    return frame.loc[matching_rows].reset_index(drop=True)