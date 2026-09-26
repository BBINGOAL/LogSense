# Detector Evaluation

## Purpose

This report compares the rule-based baseline and Isolation Forest
using the same labeled synthetic evaluation data.

The goal is to verify the evaluation flow. These results do not
represent production accuracy.

## Data split

Training and evaluation data are separated.

- Training set: 20 synthetic normal metric windows
- Evaluation set: 6 labeled metric windows
- Normal evaluation windows: 3
- Anomalous evaluation windows: 3

The anomaly examples contain:

1. high error rate
2. high p95 latency
3. high error rate, latency, and request count

## Model features

Isolation Forest uses:

- request count
- error rate
- mean latency
- p95 latency

Missing latency values are filled using the median learned from
the training data.

The model uses:

- contamination: `0.1`
- random state: `42`

## Results

| Detector | Precision | Recall | F1-score | False positives |
| --- | ---: | ---: | ---: | ---: |
| Rule-based baseline | 1.00 | 1.00 | 1.00 | 0 |
| Isolation Forest | 1.00 | 0.33 | 0.50 | 0 |

## Interpretation

The rule-based baseline detected all three synthetic anomalies.

Isolation Forest detected the most extreme anomaly but missed the
examples containing only a high error rate or high latency.

This does not prove that rule-based detection is generally better.
The synthetic anomaly labels were intentionally created from the
same error-rate and latency conditions used by the rules, so the
dataset favors the rule-based baseline.

The comparison demonstrates why a simple, explainable baseline is
useful before introducing machine learning.

## Reproduce the comparison

Run:

```powershell
python -m unittest backend.tests.test_detector_comparison -v
```

Run the complete test suite:

```powershell
python -m unittest discover -v
```

## Limitations

- The dataset is synthetic and very small.
- Labels are manually designed rather than collected from incidents.
- Results do not measure production performance.
- The model is not evaluated across different services or time ranges.
- Contamination has not been tuned using representative data.
- There is no held-out real-world dataset yet.
- Precision, recall, and F1 may change significantly with real data.

## Why ML is not in `read_log.py` yet

The current sample log produces only one metric window.

Isolation Forest needs historical windows that represent normal
behavior. Training and scoring on the same single window would not
provide meaningful anomaly detection.

The ML pipeline will be connected to the application after a larger
historical metric dataset is available.
