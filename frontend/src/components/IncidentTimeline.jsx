function formatWindowTime(timestamp, locale) {
  return new Intl.DateTimeFormat(locale, {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'UTC',
  }).format(new Date(timestamp))
}

function formatPercent(value) {
  return `${(value * 100).toFixed(0)}%`
}

function formatMilliseconds(value) {
  if (value === null || value === undefined) {
    return 'N/A'
  }

  return `${value.toLocaleString('en-US')} ms`
}

function IncidentTimeline({
  metricWindows,
  text,
  dateLocale,
}) {
  return (
    <section className="detail-section">
      <h3>{text.timeline}</h3>

      <div className="timeline-table-wrapper">
        <table className="timeline-table">
          <thead>
            <tr>
              <th scope="col">{text.windowStart}</th>
              <th scope="col">{text.requests}</th>
              <th scope="col">{text.errors}</th>
              <th scope="col">{text.errorRate}</th>
              <th scope="col">{text.p95Latency}</th>
              <th scope="col">{text.anomalyReason}</th>
            </tr>
          </thead>

          <tbody>
            {metricWindows.map((metric) => (
              <tr key={metric.window_start}>
                <td>
                  <time dateTime={metric.window_start}>
                    {formatWindowTime(
                      metric.window_start,
                      dateLocale,
                    )}{' '}
                    UTC
                  </time>
                </td>
                <td>{metric.request_count}</td>
                <td>{metric.error_count}</td>
                <td>{formatPercent(metric.error_rate)}</td>
                <td>
                  {formatMilliseconds(metric.p95_latency_ms)}
                </td>
                <td>
                  <span className="anomaly-reason">
                    {metric.anomaly_reason ?? '—'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default IncidentTimeline
