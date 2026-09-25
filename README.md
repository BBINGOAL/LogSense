# LogSense

LogSense is a learning project for analyzing application logs and detecting anomalous behavior.

## Current progress

Phase 3 — Pandas and time-window metrics

The current program can:

- Parse JSON Lines into normalized log records
- Convert normalized records into a typed Pandas DataFrame
- Preserve missing optional values
- Filter logs by level
- Group logs by service and configurable time windows
- Calculate request count, error count, and error rate
- Calculate mean and p95 latency
- Return a stable metric schema for empty input
- Report parse failures with source line numbers

## Current data flow

```text
sample.jsonl
    -> parse and validate each log
    -> NormalizedLogRecord
    -> typed Pandas DataFrame
    -> group by service and time window
    -> request, error, and latency metrics
```

This flow uses deterministic Python and Pandas logic. It does not use machine learning or an LLM.

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
- Metrics are calculated in memory and are not stored in a database
- Rule-based anomaly detection is not implemented yet
- Machine-learning anomaly detection is not implemented yet
- Evaluation metrics and labeled datasets are not implemented yet
