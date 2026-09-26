import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from backend.app.detection.ml_features import (
    select_model_features,
)


DEFAULT_CONTAMINATION = 0.1
DEFAULT_RANDOM_STATE = 42


def train_isolation_forest(
    metrics: pd.DataFrame,
    contamination: float = DEFAULT_CONTAMINATION,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> Pipeline:
    if metrics.empty:
        raise ValueError(
            "cannot train Isolation Forest with empty metrics"
        )

    if not 0.0 < contamination <= 0.5:
        raise ValueError(
            "contamination must be greater than 0.0 "
            "and less than or equal to 0.5"
        )

    features = select_model_features(metrics)

    detector = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median",
                    keep_empty_features=True,
                ),
            ),
            (
                "model",
                IsolationForest(
                    contamination=contamination,
                    random_state=random_state,
                ),
            ),
        ]
    )

    detector.fit(features)
    return detector