# LogSense

LogSense is a learning project for analyzing application logs and detecting anomalous behavior.

## Current progress

Phase 6 - Incident Engine

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
- Group nearby anomaly windows into incidents by service
- Generate deterministic incident IDs
- Track incident start time, end time, severity, and status
- Preserve anomaly triggers and evidence row indices
- Validate incident grouping columns, timestamps, and time gaps

## Current data flow

```text
JSONL logs
    -> parser and normalization
    -> typed Pandas DataFrame
    -> time-window metrics
        +-> rule-based thresholds
        |     -> rule prediction and reason
        |     -> group nearby anomalies by service
        |     -> incident with severity and evidence
        +-> model feature selection
              -> median imputation
              -> Isolation Forest
              -> anomaly score and ML prediction

labeled evaluation metrics
    -> compare predictions with ground truth
    -> precision, recall, F1-score, and false positives
```

Parsing, metrics, rules, and incident grouping use deterministic logic.
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

## Default incident rules

- Only rows marked as anomalies are grouped
- Anomalies must belong to the same service
- The maximum gap between consecutive anomalies is `10 minutes`
- A gap equal to `10 minutes` remains in the same incident
- One anomaly has low severity
- Two anomalies have medium severity
- Three or more anomalies have high severity
- New incidents start with status `open`
- Triggers and evidence indices are preserved for traceability

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
- Metrics, detector results, and incidents are stored only in memory
- Rule thresholds are configured manually
- ML evaluation uses a small synthetic labeled dataset
- There is no held-out real-world labeled dataset yet
- Isolation Forest is not connected to `read_log.py` because the sample produces only one metric window
- Incident grouping currently consumes rule-based detection results
- Severity is based only on anomaly count
- Evidence references are DataFrame indices rather than persistent database IDs
- Cross-service correlation and incident status updates are not implemented yet
