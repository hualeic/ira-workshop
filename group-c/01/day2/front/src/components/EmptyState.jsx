import { Empty } from 'antd'

export default function EmptyState({ type = 'noData' }) {
  const descriptions = {
    noData: '暂无消息',
    noFilter: '未找到匹配结果，请尝试调整筛选条件',
    noSearch: '未找到匹配结果，请尝试缩短关键词',
  }
  return <Empty description={descriptions[type] || descriptions.noData} style={{ padding: '60px 0' }} />
}
