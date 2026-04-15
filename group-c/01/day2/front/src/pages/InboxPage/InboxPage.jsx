import { List, Typography } from 'antd'
import { useMessages } from '../../hooks/useMessages'
import InboxFilters from './InboxFilters'
import MessageCard from './MessageCard'
import LoadMoreButton from './LoadMoreButton'
import SkeletonMessageList from '../../components/SkeletonMessageList'
import EmptyState from '../../components/EmptyState'
import ErrorDisplay from '../../components/ErrorDisplay'
import { useResearch } from '../../context/ResearchContext'

export default function InboxPage() {
  const { items, isLoading, error, hasMore, loadMore, refresh } = useMessages()
  const { state } = useResearch()
  const hasFilters = state.filters.unreadOnly || state.filters.category

  return (
    <div>
      <Typography.Title level={4} style={{ marginBottom: 16 }}>
        消息收件箱
      </Typography.Title>
      <InboxFilters />
      {isLoading && items.length === 0 ? (
        <SkeletonMessageList />
      ) : error && items.length === 0 ? (
        <ErrorDisplay error={error} onRetry={refresh} />
      ) : items.length === 0 ? (
        <EmptyState type={hasFilters ? 'noFilter' : 'noData'} />
      ) : (
        <>
          <List
            bordered
            dataSource={items}
            renderItem={(item) => <MessageCard key={item.messageId} item={item} />}
          />
          <LoadMoreButton hasMore={hasMore} isLoading={isLoading} onClick={loadMore} />
        </>
      )}
    </div>
  )
}
