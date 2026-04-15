import { useState } from 'react'
import { Input, DatePicker, Button, Space } from 'antd'
import { SearchOutlined } from '@ant-design/icons'

const { RangePicker } = DatePicker

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('')
  const [dateRange, setDateRange] = useState(null)

  const handleSearch = () => {
    if (!query.trim()) return
    const range = {}
    if (dateRange && dateRange[0]) range.from = dateRange[0].format('YYYY-MM-DD')
    if (dateRange && dateRange[1]) range.to = dateRange[1].format('YYYY-MM-DD')
    onSearch(query.trim(), range)
  }

  return (
    <Space wrap style={{ width: '100%', marginBottom: 16 }}>
      <Input
        placeholder="输入关键词搜索研报..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onPressEnter={handleSearch}
        prefix={<SearchOutlined />}
        allowClear
        size="large"
        style={{ width: 360 }}
      />
      <RangePicker
        value={dateRange}
        onChange={setDateRange}
        size="large"
        style={{ width: 280 }}
      />
      <Button
        type="primary"
        size="large"
        loading={loading}
        onClick={handleSearch}
        icon={<SearchOutlined />}
      >
        搜索
      </Button>
    </Space>
  )
}
