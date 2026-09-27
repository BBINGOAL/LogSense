function DashboardState({
  status,
  errorMessage,
  text,
  onRetry,
}) {
  const isLoading = status === 'loading'
  const isError = status === 'error'
  const title = isLoading
    ? text.loadingTitle
    : isError
      ? text.errorTitle
      : text.emptyTitle
  const description = isLoading
    ? text.loadingDescription
    : isError
      ? text.errorDescription
      : text.emptyDescription

  return (
    <section
      className="panel dashboard-state"
      role={isError ? 'alert' : 'status'}
    >
      <span
        className={`state-symbol state-symbol--${status}`}
        aria-hidden="true"
      >
        {isLoading ? '…' : isError ? '!' : '0'}
      </span>
      <h2>{title}</h2>
      <p>{description}</p>

      {isError && errorMessage && (
        <code className="state-error-detail">
          {errorMessage}
        </code>
      )}

      {isError && (
        <button
          type="button"
          className="retry-button"
          onClick={onRetry}
        >
          {text.retry}
        </button>
      )}
    </section>
  )
}

export default DashboardState
