import { useCallback } from 'react'
import { message } from 'antd'

export function useErrorHandler() {
  const handleError = useCallback((error) => {
    if (!error) return
    const msg = error.message || '未知错误'
    const traceId = error.traceId

    if (error.code === 'M1_RATE_LIMIT') {
      message.warning(msg)
    } else if (error.status >= 500 || error.code === 'NETWORK_ERROR') {
      message.error(traceId ? `${msg}（ID: ${traceId}）` : msg)
    } else {
      message.error(msg)
    }
  }, [])

  return { handleError }
}
