import { Typography } from 'antd'
import { useSearch } from '../../hooks/useSearch'
import SearchBar from './SearchBar'
import SearchResultList from './SearchResultList'
import LoadMoreButton from '../InboxPage/LoadMoreButton'
import SkeletonMessageList from '../../components/SkeletonMessageList'
import EmptyState from '../../components/EmptyState'
import ErrorDisplay from '../../components/ErrorDisplay'

export default function SearchPage() {
  const { items, isSearching, error, hasMore, query, search, loadMore } = useSearch()

  return (
    <div>
      <Typography.Title level={4} style={{ marginBottom: 16 }}>
        研报搜索
      </Typography.Title>
      <SearchBar onSearch={search} loading={isSearching} />
      {isSearching && items.length === 0 ? (
        <SkeletonMessageList />
      ) : error ? (
        <ErrorDisplay error={error} onRetry={() => search(query)} />
      ) : items.length > 0 ? (
        <>
          <SearchResultList items={items} />
          <LoadMoreButton hasMore={hasMore} isLoading={isSearching} onClick={loadMore} />
        </>
      ) : query ? (
        <EmptyState type="noSearch" />
      ) : null}
    </div>
  )
}
