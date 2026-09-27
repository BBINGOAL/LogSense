import IncidentTimeline from './IncidentTimeline.jsx'

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

function IncidentDetail({ record, text, dateLocale }) {
  const { incident, metric_windows: metricWindows, analysis } = record
  const metric = metricWindows[0]
  const { metadata, response } = analysis

  return (
    <section className="panel detail-panel">
      <div className="detail-header">
        <div>
          <p className="eyebrow">{text.selectedIncident}</p>
          <h2>{incident.service}</h2>
          <p className="selected-incident-id">
            {incident.incident_id}
          </p>
        </div>

        <div className="detail-badges">
          <span
            className={`severity severity--${incident.severity}`}
          >
            {text.severity[incident.severity] ?? incident.severity}
          </span>
          <span className="status-badge">
            {text.status[incident.status] ?? incident.status}
          </span>
        </div>
      </div>

      <section className="detail-section">
        <h3>{text.metricEvidence}</h3>

        <div className="metric-grid">
          <MetricCard
            label={text.requests}
            value={metric.request_count.toLocaleString('en-US')}
          />
          <MetricCard
            label={text.errors}
            value={metric.error_count.toLocaleString('en-US')}
          />
          <MetricCard
            label={text.errorRate}
            value={formatPercent(metric.error_rate)}
          />
          <MetricCard
            label={text.p95Latency}
            value={formatMilliseconds(metric.p95_latency_ms)}
          />
        </div>
      </section>

      <IncidentTimeline
        metricWindows={metricWindows}
        text={text}
        dateLocale={dateLocale}
      />

      <section className="detail-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">{text.geminiAnalysis}</p>
            <h3>{text.evidenceBasedExplanation}</h3>
          </div>
          <span className="model-name">{metadata.model}</span>
        </div>

        <p className="analysis-source-note">
          {text.analysisSourceNote}
        </p>

        <div className="analysis-block">
          <h4>{text.observedFacts}</h4>
          <ul>
            {response.observed_facts.map((fact) => (
              <li key={fact}>{fact}</li>
            ))}
          </ul>
        </div>

        <div className="analysis-block">
          <h4>{text.likelyExplanation}</h4>
          <p>{response.likely_explanation}</p>
        </div>

        <div className="uncertainty-block">
          <h4>{text.uncertainty}</h4>
          <p>{response.uncertainty}</p>
        </div>

        <div className="analysis-block">
          <h4>{text.recommendedNextChecks}</h4>
          <ol>
            {response.recommended_next_checks.map((check) => (
              <li key={check}>{check}</li>
            ))}
          </ol>
        </div>

        <footer className="analysis-metadata">
          <span>
            {text.detector}: {metadata.detector_name}
          </span>
          <span>
            {text.prompt}: {metadata.prompt_version}
          </span>
          <span>
            {text.evidenceRows}:{' '}
            {metadata.evidence_indices.join(', ')}
          </span>
        </footer>
      </section>
    </section>
  )
}

export default IncidentDetail
