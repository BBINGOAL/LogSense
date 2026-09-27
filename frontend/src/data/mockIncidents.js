export const mockIncidentRecords = [
  {
    incident: {
      incident_id: 'auth-20260927T100000Z',
      service: 'auth',
      started_at: '2026-09-27T10:00:00+00:00',
      ended_at: '2026-09-27T10:05:00+00:00',
      severity: 'high',
      triggers: ['high_error_rate', 'high_latency'],
      evidence_indices: [7],
      status: 'open',
    },
    metric_windows: [
      {
        window_start: '2026-09-27T10:00:00+00:00',
        request_count: 100,
        error_count: 65,
        error_rate: 0.65,
        mean_latency_ms: 720,
        p95_latency_ms: 1400,
        anomaly_reason: 'high_error_rate, high_latency',
        anomaly_score: null,
      },
    ],
    analysis: {
      metadata: {
        incident_id: 'auth-20260927T100000Z',
        detector_name: 'rule_based',
        model: 'gemini-3.8-flash',
        prompt_version: 'incident-analysis-v2',
        evidence_indices: [7],
      },
      response: {
        observed_facts: [
          'The auth service error rate was 65%.',
          'The p95 latency was 1400 ms.',
        ],
        likely_explanation:
          'The auth service experienced elevated failures and latency.',
        uncertainty:
          'No stack trace or dependency metrics were supplied.',
        recommended_next_checks: [
          'Inspect auth application error logs.',
          'Check downstream identity-provider health.',
        ],
      },
    },
  },
]