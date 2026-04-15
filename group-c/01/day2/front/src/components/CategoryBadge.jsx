import { Tag } from 'antd'
import { CATEGORY_COLORS } from '../constants'

export default function CategoryBadge({ category }) {
  if (!category) return null
  const color = CATEGORY_COLORS[category] || 'default'
  return <Tag color={color}>{category}</Tag>
}
