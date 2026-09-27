import { useCallback, useEffect, useState } from 'react'
import { fetchIncidentRecords } from '../api/incidents.js'

function getErrorMessage(error) {
  if (error instanceof Error) {
    return error.message
  }

  return String(error)
}

export function useIncidentRecords() {
  const [records, setRecords] = useState([])
  const [status, setStatus] = useState('loading')
  const [errorMessage, setErrorMessage] = useState('')
  const [requestNumber, setRequestNumber] = useState(0)

  const retry = useCallback(() => {
    setStatus('loading')
    setErrorMessage('')
    setRequestNumber((current) => current + 1)
  }, [])

  useEffect(() => {
    const controller = new AbortController()

    fetchIncidentRecords({ signal: controller.signal })
      .then((loadedRecords) => {
        setRecords(loadedRecords)
        setStatus(
          loadedRecords.length === 0 ? 'empty' : 'success',
        )
      })
      .catch((error) => {
        if (error.name === 'AbortError') {
          return
        }

        setRecords([])
        setErrorMessage(getErrorMessage(error))
        setStatus('error')
      })

    return () => controller.abort()
  }, [requestNumber])

  return {
    records,
    status,
    errorMessage,
    retry,
  }
}
