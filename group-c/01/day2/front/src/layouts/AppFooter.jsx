import { Layout } from 'antd'
import { DISCLAIMER_TEXT } from '../constants'

export default function AppFooter() {
  return (
    <Layout.Footer
      style={{
        textAlign: 'center',
        fontSize: 12,
        color: '#999',
        padding: '16px 24px',
        background: 'transparent',
        borderTop: '1px solid #f0f0f0',
        marginTop: 24,
      }}
    >
      {DISCLAIMER_TEXT}
    </Layout.Footer>
  )
}
