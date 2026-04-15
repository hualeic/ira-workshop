import { Button } from 'antd'

export default function LoadMoreButton({ hasMore, isLoading, onClick }) {
  if (!hasMore) return null
  return (
    <div style={{ textAlign: 'center', padding: '16px 0' }}>
      <Button onClick={onClick} loading={isLoading}>
        加载更多
      </Button>
    </div>
  )
}
