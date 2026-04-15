import { Space, Switch, Select, Typography } from 'antd'
import { useResearch } from '../../context/ResearchContext'
import { CATEGORY_COLORS } from '../../constants'

const categoryOptions = Object.keys(CATEGORY_COLORS).map((c) => ({ label: c, value: c }))

export default function InboxFilters() {
  const { state, dispatch } = useResearch()
  const { filters } = state

  return (
    <Space wrap style={{ marginBottom: 16 }}>
      <Space>
        <Typography.Text>仅未读</Typography.Text>
        <Switch
          checked={filters.unreadOnly}
          onChange={(checked) =>
            dispatch({ type: 'SET_FILTERS', payload: { unreadOnly: checked } })
          }
        />
      </Space>
      <Select
        placeholder="按类别筛选"
        allowClear
        value={filters.category}
        onChange={(value) =>
          dispatch({ type: 'SET_FILTERS', payload: { category: value || null } })
        }
        options={categoryOptions}
        style={{ width: 160 }}
      />
    </Space>
  )
}
