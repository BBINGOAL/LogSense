import { useState } from 'react'
import IncidentDetail from './components/IncidentDetail.jsx'
import { mockIncidentRecords } from './data/mockIncidents.js'
import {
  dateLocales,
  translations,
} from './i18n/translations.js'
import './App.css'

function formatTimestamp(timestamp, locale) {
  return new Intl.DateTimeFormat(locale, {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC',
  }).format(new Date(timestamp))
}

function App() {
  const [language, setLanguage] = useState('th')
  const selectedRecord = mockIncidentRecords[0]
  const text = translations[language]
  const dateLocale = dateLocales[language]

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">LogSense</p>
          <h1>{text.dashboardTitle}</h1>
          <p className="header-description">
            {text.dashboardDescription}
          </p>
        </div>

        <div className="header-actions">
          <div className="data-status">
            <span className="status-dot" />
            {text.localMockData}
          </div>

          <div
            className="language-switcher"
            aria-label={text.languageSelector}
          >
            <button
              type="button"
              aria-pressed={language === 'th'}
              onClick={() => setLanguage('th')}
            >
              TH
            </button>
            <button
              type="button"
              aria-pressed={language === 'en'}
              onClick={() => setLanguage('en')}
            >
              EN
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-layout">
        <aside className="panel incident-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">{text.monitoring}</p>
              <h2>{text.incidents}</h2>
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
                    {text.severity[incident.severity] ??
                      incident.severity}
                  </span>
                </div>

                <p className="incident-id">
                  {incident.incident_id}
                </p>

                <time dateTime={incident.started_at}>
                  {formatTimestamp(
                    incident.started_at,
                    dateLocale,
                  )}{' '}
                  UTC
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

        <IncidentDetail
          record={selectedRecord}
          text={text}
        />
      </main>
    </div>
  )
}

export default App