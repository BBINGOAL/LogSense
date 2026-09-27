export async function fetchIncidentRecords({ signal } = {}) {
  const response = await fetch('/api/incidents', { signal })

  if (!response.ok) {
    throw new Error(
      `Incident API returned HTTP ${response.status}`,
    )
  }

  const records = await response.json()

  if (!Array.isArray(records)) {
    throw new Error('Incident API response must be an array')
  }

  return records
}
