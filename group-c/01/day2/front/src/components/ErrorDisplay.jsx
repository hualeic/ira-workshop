import { Result, Typography, Button } from 'antd'
import TraceIdCopy from './TraceIdCopy'

export default function ErrorDisplay({ error, onRetry }) {
  return (
    <Result
      status="error"
      title={error?.message || '发生错误'}
      subTitle={error?.traceId && <TraceIdCopy traceId={error.traceId} />}
      extra={
        onRetry && (
          <Button type="primary" onClick={onRetry}>
            重试
          </Button>
        )
      }
    />
  )
}
