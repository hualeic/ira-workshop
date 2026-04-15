import { List } from 'antd'
import MessageCard from '../InboxPage/MessageCard'

export default function SearchResultList({ items }) {
  return (
    <List
      bordered
      dataSource={items}
      renderItem={(item) => (
        <MessageCard key={item.messageId} item={item} showHighlight />
      )}
    />
  )
}
