import { Skeleton, List } from 'antd'

export default function SkeletonMessageList({ count = 5 }) {
  return (
    <List
      dataSource={Array.from({ length: count })}
      renderItem={(_, i) => (
        <List.Item key={i}>
          <Skeleton active paragraph={{ rows: 2 }} />
        </List.Item>
      )}
    />
  )
}
