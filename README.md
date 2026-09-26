# LogSense

LogSense is a learning project for analyzing application logs and detecting anomalous behavior.

## Current progress

Phase 5 - Isolation Forest and evaluation

The current program can:

- Parse JSON Lines into normalized log records
- Convert normalized records into a typed Pandas DataFrame
- Preserve missing optional values
- Filter logs by level
- Group logs by service and configurable time windows
- Calculate request count, error count, and error rate
- Calculate mean and p95 latency
- Detect high error rates using a configurable threshold
- Detect high p95 latency using a configurable threshold
- Combine multiple rule results into one anomaly decision
- Preserve the rule reasons for each detected anomaly
- Reject invalid threshold values
- Report parse failures with source line numbers
- Select numerical features for machine-learning detection
- Fill missing latency using training-data medians
- Train and score an Isolation Forest with reproducible settings
- Calculate precision, recall, F1-score, and false positives
- Compare Isolation Forest with the rule-based baseline

## Current data flow

```text
JSONL logs
    -> parser and normalization
    -> typed Pandas DataFrame
    -> time-window metrics
        ├── rule-based thresholds
        │     -> rule prediction and reason
        └── model feature selection
              -> median imputation
              -> Isolation Forest
              -> anomaly score and ML prediction

labeled evaluation metrics
    -> compare predictions with ground truth
    -> precision, recall, F1-score, and false positives
```

Parsing, metrics, and rule detection use deterministic logic.
Isolation Forest provides the machine-learning detection branch.
The project does not use an LLM yet.

## Default anomaly rules

- Error rate greater than or equal to `0.5`
- P95 latency greater than or equal to `500 ms`
- Missing latency is not treated as a latency anomaly

## Default model settings

- Features: request count, error rate, mean latency, and p95 latency
- Missing latency strategy: training-data median
- Contamination: `0.1`
- Random state: `42`
- Feature scaling: not required for the tree-based detector

See [Detector evaluation](docs/evaluation.md) for the current
synthetic-data comparison and limitations.

## Requirements

- Python 3.11 or newer

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python read_log.py
```

## Tests

```powershell
python -m unittest discover -v
```

## Current limitations

- Field value types are not fully validated yet
- Metrics and detection results are stored only in memory
- Rule thresholds are configured manually
- ML evaluation uses a small synthetic labeled dataset
- There is no held-out real-world labeled dataset yet
- Isolation Forest is not connected to `read_log.py` because the sample produces only one metric window
- Detector performance has not been validated across different services or time ranges
