import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { antdTheme } from './theme/antdTheme'
import { ResearchProvider } from './context/ResearchContext'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <ConfigProvider theme={antdTheme} locale={zhCN}>
        <ResearchProvider>
          <App />
        </ResearchProvider>
      </ConfigProvider>
    </BrowserRouter>
  </StrictMode>,
)
