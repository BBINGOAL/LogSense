# LogSense frontend

The Phase 8 dashboard is a React application built with Vite. It loads
incident records from `GET /api/incidents` and displays the selected
incident's metrics, evidence timeline, and evidence-based LLM analysis.

## Development

Start the LogSense backend from the repository root first:

```powershell
python -m uvicorn backend.app.api.main:app --reload
```

Then run the frontend in this directory:

```powershell
npm install
npm run dev
```

Vite proxies `/api` to `http://127.0.0.1:8000` during development.

## Checks

```powershell
npm run lint
npm run build
```

The dashboard supports Thai and English interface labels. Gemini
analysis content remains in canonical English so the stored analysis is
not changed by presentation-language selection.
