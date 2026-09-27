function formatPercent(value) {
  return `${(value * 100).toFixed(0)}%`
}

function formatMilliseconds(value) {
  if (value === null || value === undefined) {
    return 'N/A'
  }

  return `${value.toLocaleString('en-US')} ms`
}

function MetricCard({ label, value }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function IncidentDetail({ record }) {
  const { incident, metric_windows: metricWindows, analysis } = record
  const metric = metricWindows[0]
  const { metadata, response } = analysis

  return (
    <section className="panel detail-panel">
      <div className="detail-header">
        <div>
          <p className="eyebrow">Selected incident</p>
          <h2>{incident.service}</h2>
          <p className="selected-incident-id">
            {incident.incident_id}
          </p>
        </div>

        <div className="detail-badges">
          <span
            className={`severity severity--${incident.severity}`}
          >
            {incident.severity}
          </span>
          <span className="status-badge">{incident.status}</span>
        </div>
      </div>

      <section className="detail-section">
        <h3>Metric evidence</h3>

        <div className="metric-grid">
          <MetricCard
            label="Requests"
            value={metric.request_count.toLocaleString('en-US')}
          />
          <MetricCard
            label="Errors"
            value={metric.error_count.toLocaleString('en-US')}
          />
          <MetricCard
            label="Error rate"
            value={formatPercent(metric.error_rate)}
          />
          <MetricCard
            label="P95 latency"
            value={formatMilliseconds(metric.p95_latency_ms)}
          />
        </div>
      </section>

      <section className="detail-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Gemini analysis</p>
            <h3>Evidence-based explanation</h3>
          </div>
          <span className="model-name">{metadata.model}</span>
        </div>

        <div className="analysis-block">
          <h4>Observed facts</h4>
          <ul>
            {response.observed_facts.map((fact) => (
              <li key={fact}>{fact}</li>
            ))}
          </ul>
        </div>

        <div className="analysis-block">
          <h4>Likely explanation</h4>
          <p>{response.likely_explanation}</p>
        </div>

        <div className="uncertainty-block">
          <h4>Uncertainty</h4>
          <p>{response.uncertainty}</p>
        </div>

        <div className="analysis-block">
          <h4>Recommended next checks</h4>
          <ol>
            {response.recommended_next_checks.map((check) => (
              <li key={check}>{check}</li>
            ))}
          </ol>
        </div>

        <footer className="analysis-metadata">
          <span>Detector: {metadata.detector_name}</span>
          <span>Prompt: {metadata.prompt_version}</span>
          <span>
            Evidence rows: {metadata.evidence_indices.join(', ')}
          </span>
        </footer>
      </section>
    </section>
  )
}

export default IncidentDetail