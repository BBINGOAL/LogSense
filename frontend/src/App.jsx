import './App.css'
import { mockIncidentRecords } from './data/mockIncidents.js'

function formatTimestamp(timestamp) {
  return new Intl.DateTimeFormat('en-GB', {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC',
  }).format(new Date(timestamp))
}

function App() {
  const selectedRecord = mockIncidentRecords[0]
  const selectedIncident = selectedRecord.incident

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">LogSense</p>
          <h1>Incident Dashboard</h1>
          <p className="header-description">
            Review detected anomalies, supporting evidence, and
            AI-generated explanations.
          </p>
        </div>

        <div className="data-status">
          <span className="status-dot" />
          Local mock data
        </div>
      </header>

      <main className="dashboard-layout">
        <aside className="panel incident-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Monitoring</p>
              <h2>Incidents</h2>
            </div>

            <span className="incident-count">
              {mockIncidentRecords.length}
            </span>
          </div>

          <div className="incident-list">
            {mockIncidentRecords.map(({ incident }) => (
              <article
                className="incident-card incident-card--active"
                key={incident.incident_id}
              >
                <div className="incident-card-header">
                  <strong>{incident.service}</strong>
                  <span
                    className={`severity severity--${incident.severity}`}
                  >
                    {incident.severity}
                  </span>
                </div>

                <p className="incident-id">
                  {incident.incident_id}
                </p>

                <time dateTime={incident.started_at}>
                  {formatTimestamp(incident.started_at)} UTC
                </time>

                <div className="trigger-list">
                  {incident.triggers.map((trigger) => (
                    <span className="trigger" key={trigger}>
                      {trigger}
                    </span>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </aside>

        <section className="panel detail-panel">
          <p className="eyebrow">Selected incident</p>
          <h2>{selectedIncident.service}</h2>
          <p className="selected-incident-id">
            {selectedIncident.incident_id}
          </p>
          <p className="detail-placeholder">
            Metrics, evidence, and the Gemini analysis will appear
            here in the next step.
          </p>
        </section>
      </main>
    </div>
  )
}

export default App