import { Typography, Space } from 'antd'
import { LinkOutlined } from '@ant-design/icons'

export default function LinksSection({ links }) {
  if (!links || links.length === 0) return null

  return (
    <div style={{ marginTop: 16 }}>
      <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
        相关链接
      </Typography.Text>
      <Space direction="vertical" size={4}>
        {links.map((link, index) => (
          <a
            key={index}
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{ display: 'flex', alignItems: 'center', gap: 4 }}
          >
            <LinkOutlined />
            {link.label || link.url}
          </a>
        ))}
      </Space>
    </div>
  )
}
