import { Typography, message as antMsg } from 'antd'
import { CopyOutlined } from '@ant-design/icons'

export default function TraceIdCopy({ traceId }) {
  if (!traceId) return null
  const handleCopy = () => {
    navigator.clipboard.writeText(traceId).then(() => antMsg.success('已复制'))
  }
  return (
    <Typography.Text code style={{ cursor: 'pointer', fontSize: 12 }} onClick={handleCopy}>
      {traceId} <CopyOutlined />
    </Typography.Text>
  )
}
