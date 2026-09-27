# LogSense

LogSense is a learning project for analyzing application logs and detecting anomalous behavior.

## Current progress

Phase 8 - React Dashboard

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
- Build evidence bundles from incident detection rows
- Generate deterministic, versioned incident-analysis prompts
- Treat log samples as untrusted prompt data
- Request structured JSON analysis from Gemini
- Validate malformed and incomplete model responses
- Separate observed facts, likely explanations, uncertainty, and next checks
- Track the incident, detector, model, prompt version, and evidence indices
- Run the complete LLM pipeline with a fake API boundary in automated tests
- Serve typed incident records from a FastAPI endpoint
- Load dashboard data through a React API client
- Display incident metrics, evidence timeline, and LLM analysis
- Switch dashboard interface labels between Thai and English
- Display loading, error, empty, and successful data states
- Retry a failed dashboard API request

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
        |     -> evidence bundle
        |     -> versioned English analysis prompt
        |     -> Gemini structured response
        |     -> schema validation
        |     -> analysis result with audit metadata
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
Gemini provides evidence-based incident explanations after deterministic
detection and grouping. The LLM does not decide whether a metric window
is anomalous.

LLM analysis is stored as canonical English content. Translation belongs
to the dashboard presentation layer and is not part of the analysis
pipeline.

The Phase 8 dashboard currently consumes deterministic in-memory sample
incident records through the API. This keeps the HTTP and UI flow
testable before persistent storage is introduced.

```text
in-memory incident records
    -> GET /api/incidents
    -> React API client
    -> loading / error / empty / success state
    -> incident list and selected incident
    -> metrics, evidence timeline, and LLM explanation
```

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

## LLM analysis rules

- Model: `gemini-3.8-flash`
- Prompt version: `incident-analysis-v2`
- Only supplied incident evidence may be used
- Identifiers such as `incident_id` must not be treated as root-cause evidence
- Log samples are untrusted data, not instructions
- Response values use English while JSON field names remain stable
- Responses must contain observed facts, likely explanation, uncertainty,
  and recommended next checks
- Analysis metadata records the incident, detector, model, prompt version,
  and evidence row indices
- Automated tests use a fake Gemini boundary and do not consume API quota

## Requirements

- Python 3.11 or newer
- Node.js 20.19 or newer

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

Install frontend dependencies:

```powershell
cd frontend
npm install
cd ..
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Set the Gemini API key inside `.env`:

```dotenv
GEMINI_API_KEY=your_real_key_here
```

The `.env` file is ignored by Git and must never be committed.
A Gemini key is required only for live LLM requests; automated tests
do not call the external API.

## Run the dashboard

Start the backend API from the repository root:

```powershell
python -m uvicorn backend.app.api.main:app --reload
```

In a second terminal, start the React development server:

```powershell
cd frontend
npm run dev
```

Open the local URL printed by Vite, normally
`http://localhost:5173`. Vite proxies `/api` requests to the backend at
`http://127.0.0.1:8000`.

The API documentation is available while the backend is running at
`http://127.0.0.1:8000/docs`.

## Run the log parsing example

```powershell
python read_log.py
```

## Tests

```powershell
python -m unittest discover -s backend/tests -v
```

Check the frontend:

```powershell
cd frontend
npm run lint
npm run build
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
- LLM analyses and metadata are stored only in memory
- LLM output can still be incorrect and requires human review
- Raw prompts and evidence bundles are not persisted
- The dashboard API serves sample incident records and is not connected
  to the full detection pipeline or a database yet
- Thai/English switching translates interface labels, while canonical
  LLM analysis remains in English
- Frontend component tests are not configured yet
- Gemini is the only configured LLM provider
