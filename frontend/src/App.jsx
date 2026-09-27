import './App.css'
import { mockIncidentRecords } from './data/mockIncidents.js'

function App() {
  const incidentCount = mockIncidentRecords.length

  return (
    <main>
      <p>LogSense</p>
      <h1>Incident Dashboard</h1>
      <p>
        {incidentCount} incident
        {incidentCount === 1 ? '' : 's'} loaded from local mock data.
      </p>
    </main>
  )
}

export default App