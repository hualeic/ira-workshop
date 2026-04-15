import { Layout, Typography, Badge } from 'antd'
import { FundOutlined } from '@ant-design/icons'
import { useEffect, useState } from 'react'
import { checkHealth } from '../api/researchApi'

const { Header } = Layout

export default function AppHeader() {
  const [healthy, setHealthy] = useState(null)

  useEffect(() => {
    checkHealth()
      .then(() => setHealthy(true))
      .catch(() => setHealthy(false))
  }, [])

  return (
    <Header
      style={{
        background: '#003399',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 24px',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <FundOutlined style={{ color: '#fff', fontSize: 24 }} />
        <Typography.Title level={4} style={{ color: '#fff', margin: 0 }}>
          投研消息中心
        </Typography.Title>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <Badge status={healthy === true ? 'success' : healthy === false ? 'error' : 'processing'} />
        <span style={{ color: '#ffffffaa', fontSize: 12 }}>
          {healthy === true ? '服务正常' : healthy === false ? '服务异常' : '检测中...'}
        </span>
      </div>
    </Header>
  )
}
