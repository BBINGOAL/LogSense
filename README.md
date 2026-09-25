# LogSense

LogSense is a learning project for analyzing application logs and detecting anomalous behavior.

## Current progress

Phase 2 — Structured log parser

The current program can:

- Read JSON Lines (`.jsonl`) one record at a time
- Parse valid JSON into a `NormalizedLogRecord`
- Normalize timestamps to UTC
- Normalize log levels to uppercase
- Support optional request ID, status code, and latency fields
- Report malformed JSON and missing required fields
- Report invalid timestamps and missing timezone information
- Preserve the source line number when reporting file errors

## Current data flow

```text
sample.jsonl
    -> read one source line
    -> parse JSON
    -> validate required fields
    -> normalize timestamp and log level
    -> NormalizedLogRecord
    -> print normalized output or parse failure
```

This flow uses deterministic Python logic. It does not use machine learning or an LLM.

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
- Parsed records are not stored in a database
- Time-window metrics are not implemented yet
- Anomaly detection is not implemented yet
