import { useNavigate } from 'react-router-dom'
import { List, Typography, Badge } from 'antd'
import { ClockCircleOutlined } from '@ant-design/icons'
import CategoryBadge from '../../components/CategoryBadge'
import dayjs from 'dayjs'

export default function MessageCard({ item, showHighlight = false }) {
  const navigate = useNavigate()

  return (
    <List.Item
      style={{ cursor: 'pointer', padding: '12px 16px' }}
      onClick={() => navigate(`/research/messages/${item.messageId}`)}
    >
      <div style={{ width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
          {!item.read && (
            <Badge
              status="processing"
              color="#003399"
              style={{ flexShrink: 0 }}
            />
          )}
          <Typography.Text
            strong={!item.read}
            style={{ fontSize: 15, flex: 1 }}
            ellipsis
          >
            {item.title}
          </Typography.Text>
          <CategoryBadge category={item.category} />
        </div>
        {item.summary && (
          <Typography.Paragraph
            type="secondary"
            ellipsis={{ rows: 2 }}
            style={{ marginBottom: 4, fontSize: 13, marginLeft: item.read ? 0 : 14 }}
          >
            {item.summary}
          </Typography.Paragraph>
        )}
        {showHighlight && item.highlight && (
          <div
            style={{
              fontSize: 13,
              color: '#666',
              background: '#fafafa',
              padding: '4px 8px',
              borderRadius: 4,
              marginBottom: 4,
              marginLeft: item.read ? 0 : 14,
            }}
            dangerouslySetInnerHTML={{ __html: item.highlight }}
          />
        )}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 12, color: '#999', marginLeft: item.read ? 0 : 14 }}>
          <span>
            <ClockCircleOutlined style={{ marginRight: 4 }} />
            {dayjs(item.publishedAt).format('YYYY-MM-DD HH:mm')}
          </span>
          {item.sourceName && <span>{item.sourceName}</span>}
          {item.read && <span style={{ color: '#52c41a' }}>已读</span>}
        </div>
      </div>
    </List.Item>
  )
}
