from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.sample_data import (
    DASHBOARD_INCIDENT_RECORDS,
)
from backend.app.api.schemas import DashboardIncidentRecord


app = FastAPI(
    title="LogSense API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get(
    "/api/incidents",
    response_model=list[DashboardIncidentRecord],
)
def list_incidents() -> list[DashboardIncidentRecord]:
    """Return incident records prepared for the dashboard."""
    return list(DASHBOARD_INCIDENT_RECORDS)
