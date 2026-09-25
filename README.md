# LogSense

LogSense is a learning project for analyzing application logs and detecting anomalous behavior.

## Current progress

Phase 4 - Rule-based anomaly detection

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

## Current data flow

```text
sample.jsonl
    -> parse and validate each log
    -> NormalizedLogRecord
    -> typed Pandas DataFrame
    -> group by service and time window
    -> request, error, and latency metrics
    -> error-rate and p95-latency rules
    -> anomaly flag and evidence-based reason
```

This flow uses deterministic Python and Pandas logic. It does not use machine learning or an LLM.

## Default anomaly rules

- Error rate greater than or equal to `0.5`
- P95 latency greater than or equal to `500 ms`
- Missing latency is not treated as a latency anomaly

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
- Rule thresholds are configured manually and do not learn from historical data
- Machine-learning anomaly detection is not implemented yet
- Evaluation metrics and labeled datasets are not implemented yet
