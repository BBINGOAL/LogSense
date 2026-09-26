from collections.abc import Sequence
from dataclasses import dataclass

from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score as calculate_f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


@dataclass(frozen=True)
class EvaluationReport:
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int


def evaluate_predictions(
    actual: Sequence[bool],
    predicted: Sequence[bool],
) -> EvaluationReport:
    actual_values = list(actual)
    predicted_values = list(predicted)

    if not actual_values:
        raise ValueError(
            "evaluation requires at least one label"
        )

    if len(actual_values) != len(predicted_values):
        raise ValueError(
            "actual and predicted labels must have equal length"
        )

    true_negatives, false_positives, false_negatives, true_positives = (
        confusion_matrix(
            actual_values,
            predicted_values,
            labels=[False, True],
        ).ravel()
    )

    return EvaluationReport(
        precision=float(
            precision_score(
                actual_values,
                predicted_values,
                zero_division=0,
            )
        ),
        recall=float(
            recall_score(
                actual_values,
                predicted_values,
                zero_division=0,
            )
        ),
        f1_score=float(
            calculate_f1_score(
                actual_values,
                predicted_values,
                zero_division=0,
            )
        ),
        true_positives=int(true_positives),
        false_positives=int(false_positives),
        false_negatives=int(false_negatives),
        true_negatives=int(true_negatives),
    )