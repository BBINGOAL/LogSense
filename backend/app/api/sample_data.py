from datetime import datetime, timezone

from backend.app.api.schemas import (
    DashboardAnalysis,
    DashboardAnalysisMetadata,
    DashboardAnalysisResponse,
    DashboardIncident,
    DashboardIncidentRecord,
    DashboardMetricWindow,
)


DASHBOARD_INCIDENT_RECORDS = (
    DashboardIncidentRecord(
        incident=DashboardIncident(
            incident_id="auth-20260927T100000Z",
            service="auth",
            started_at=datetime(
                2026, 9, 27, 10, 0, tzinfo=timezone.utc
            ),
            ended_at=datetime(
                2026, 9, 27, 10, 10, tzinfo=timezone.utc
            ),
            severity="high",
            triggers=["high_error_rate", "high_latency"],
            evidence_indices=[7, 8, 9],
            status="open",
        ),
        metric_windows=[
            DashboardMetricWindow(
                window_start=datetime(
                    2026, 9, 27, 10, 0, tzinfo=timezone.utc
                ),
                request_count=100,
                error_count=65,
                error_rate=0.65,
                mean_latency_ms=720,
                p95_latency_ms=1400,
                anomaly_reason=(
                    "high_error_rate, high_latency"
                ),
            ),
            DashboardMetricWindow(
                window_start=datetime(
                    2026, 9, 27, 10, 5, tzinfo=timezone.utc
                ),
                request_count=120,
                error_count=54,
                error_rate=0.45,
                mean_latency_ms=610,
                p95_latency_ms=1100,
                anomaly_reason="high_latency",
            ),
            DashboardMetricWindow(
                window_start=datetime(
                    2026, 9, 27, 10, 10, tzinfo=timezone.utc
                ),
                request_count=90,
                error_count=18,
                error_rate=0.2,
                mean_latency_ms=300,
                p95_latency_ms=620,
                anomaly_reason="high_latency",
            ),
        ],
        analysis=DashboardAnalysis(
            metadata=DashboardAnalysisMetadata(
                incident_id="auth-20260927T100000Z",
                detector_name="rule_based",
                model="gemini-3.8-flash",
                prompt_version="incident-analysis-v2",
                evidence_indices=[7, 8, 9],
            ),
            response=DashboardAnalysisResponse(
                observed_facts=[
                    (
                        "The auth incident contains three "
                        "anomalous metric windows."
                    ),
                    "The error rate decreased from 65% to 20%.",
                    (
                        "The p95 latency decreased from "
                        "1400 ms to 620 ms."
                    ),
                ],
                likely_explanation=(
                    "The auth service experienced elevated "
                    "failures and latency."
                ),
                uncertainty=(
                    "No stack trace or dependency metrics "
                    "were supplied."
                ),
                recommended_next_checks=[
                    "Inspect auth application error logs.",
                    (
                        "Check downstream identity-provider "
                        "health."
                    ),
                ],
            ),
        ),
    ),
    DashboardIncidentRecord(
        incident=DashboardIncident(
            incident_id="payment-20260927T101500Z",
            service="payment",
            started_at=datetime(
                2026, 9, 27, 10, 15, tzinfo=timezone.utc
            ),
            ended_at=datetime(
                2026, 9, 27, 10, 15, tzinfo=timezone.utc
            ),
            severity="low",
            triggers=["high_latency"],
            evidence_indices=[12],
            status="resolved",
        ),
        metric_windows=[
            DashboardMetricWindow(
                window_start=datetime(
                    2026, 9, 27, 10, 15, tzinfo=timezone.utc
                ),
                request_count=40,
                error_count=1,
                error_rate=0.025,
                mean_latency_ms=420,
                p95_latency_ms=780,
                anomaly_reason="high_latency",
            ),
        ],
        analysis=DashboardAnalysis(
            metadata=DashboardAnalysisMetadata(
                incident_id="payment-20260927T101500Z",
                detector_name="rule_based",
                model="gemini-3.8-flash",
                prompt_version="incident-analysis-v2",
                evidence_indices=[12],
            ),
            response=DashboardAnalysisResponse(
                observed_facts=[
                    "The payment service p95 latency was 780 ms.",
                    "The error rate was 2.5%.",
                ],
                likely_explanation=(
                    "The payment service experienced elevated "
                    "response latency."
                ),
                uncertainty=(
                    "No dependency traces or database metrics "
                    "were supplied."
                ),
                recommended_next_checks=[
                    "Inspect payment dependency latency.",
                    "Review database query duration.",
                ],
            ),
        ),
    ),
)
