import { Button } from 'antd'
import { CheckOutlined, EyeOutlined } from '@ant-design/icons'

export default function ReadStatusButton({ read, onMarkRead }) {
  if (read) {
    return (
      <Button type="text" icon={<CheckOutlined />} disabled style={{ color: '#52c41a' }}>
        已读
      </Button>
    )
  }

  return (
    <Button type="primary" icon={<EyeOutlined />} onClick={onMarkRead}>
      标记已读
    </Button>
  )
}
