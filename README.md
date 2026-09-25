# LogSense

LogSense is a learning project for analyzing application logs and detecting anomalous behavior.

## Current progress

Phase 1 — Python and log fundamentals

The current program can:

- Read JSON Lines (`.jsonl`) one record at a time
- Convert JSON text into a Python dictionary
- Convert timestamps with a timezone to UTC
- Report malformed JSON with its source line number
- Report timestamps that do not contain timezone information

## Current data flow

```text
sample.jsonl
    -> read one line
    -> parse JSON
    -> convert timestamp to UTC
    -> print normalized output or parse error
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
python -m unittest test_read_log.py -v
```

## Current limitations

- Required log fields are not validated yet
- Invalid timestamp formats are not handled yet
- Parsed records are not stored in a database
- Anomaly detection is not implemented yet