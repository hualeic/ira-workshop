import { Layout, Menu } from 'antd'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { InboxOutlined, SearchOutlined } from '@ant-design/icons'
import AppHeader from './AppHeader'
import AppFooter from './AppFooter'

const { Sider, Content } = Layout

const menuItems = [
  { key: '/research/inbox', icon: <InboxOutlined />, label: '消息收件箱' },
  { key: '/research/search', icon: <SearchOutlined />, label: '搜索' },
]

export default function AppLayout() {
  const navigate = useNavigate()
  const location = useLocation()

  const selectedKey = menuItems.find((item) => location.pathname.startsWith(item.key))?.key || '/research/inbox'

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <AppHeader />
      <Layout>
        <Sider
          width={200}
          breakpoint="md"
          collapsedWidth={60}
          style={{ background: '#fff', borderRight: '1px solid #f0f0f0' }}
        >
          <Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            items={menuItems}
            onClick={({ key }) => navigate(key)}
            style={{ height: '100%', borderRight: 0, paddingTop: 8 }}
          />
        </Sider>
        <Layout style={{ padding: '24px' }}>
          <Content style={{ background: '#fff', padding: 24, borderRadius: 8, minHeight: 400 }}>
            <Outlet />
          </Content>
          <AppFooter />
        </Layout>
      </Layout>
    </Layout>
  )
}
