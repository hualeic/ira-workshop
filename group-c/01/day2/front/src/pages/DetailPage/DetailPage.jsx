import { useParams, useNavigate } from 'react-router-dom'
import { Typography, Divider, Skeleton, Button, Space } from 'antd'
import { ArrowLeftOutlined, ClockCircleOutlined } from '@ant-design/icons'
import { useMessageDetail } from '../../hooks/useMessageDetail'
import MessageBody from './MessageBody'
import LinksSection from './LinksSection'
import ReadStatusButton from './ReadStatusButton'
import CategoryBadge from '../../components/CategoryBadge'
import ErrorDisplay from '../../components/ErrorDisplay'
import dayjs from 'dayjs'

export default function DetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { message, isLoading, error, markAsRead } = useMessageDetail(id)

  if (isLoading) {
    return (
      <div style={{ padding: '16px 0' }}>
        <Skeleton active paragraph={{ rows: 8 }} />
      </div>
    )
  }

  if (error) {
    return <ErrorDisplay error={error} onRetry={() => navigate(0)} />
  }

  if (!message) return null

  return (
    <div>
      <Button
        type="link"
        icon={<ArrowLeftOutlined />}
        onClick={() => navigate(-1)}
        style={{ padding: 0, marginBottom: 16 }}
      >
        返回
      </Button>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <Typography.Title level={4} style={{ margin: 0, flex: 1 }}>
          {message.title}
        </Typography.Title>
        <ReadStatusButton read={message.read} onMarkRead={markAsRead} />
      </div>

      <Space size={16} style={{ color: '#999', fontSize: 13, marginBottom: 16 }}>
        <span>
          <ClockCircleOutlined style={{ marginRight: 4 }} />
          {dayjs(message.publishedAt).format('YYYY-MM-DD HH:mm')}
        </span>
        {message.sourceName && <span>{message.sourceType}: {message.sourceName}</span>}
        <CategoryBadge category={message.category} />
      </Space>

      {message.summary && (
        <Typography.Paragraph type="secondary" style={{ marginTop: 8, fontSize: 14, background: '#fafafa', padding: '12px 16px', borderRadius: 6 }}>
          {message.summary}
        </Typography.Paragraph>
      )}

      <Divider />

      <MessageBody body={message.body} contentFormat={message.contentFormat} />

      <LinksSection links={message.links} />

      {message.metadata && Object.keys(message.metadata).length > 0 && (
        <div style={{ marginTop: 16, padding: '8px 12px', background: '#f5f5f5', borderRadius: 4, fontSize: 12, color: '#999' }}>
          {Object.entries(message.metadata).map(([key, val]) => (
            <span key={key} style={{ marginRight: 16 }}>{key}: {val}</span>
          ))}
        </div>
      )}
    </div>
  )
}
