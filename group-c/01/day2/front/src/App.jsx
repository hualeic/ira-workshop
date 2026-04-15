import { Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import InboxPage from './pages/InboxPage/InboxPage'
import SearchPage from './pages/SearchPage/SearchPage'
import DetailPage from './pages/DetailPage/DetailPage'
import NotFoundPage from './pages/ErrorPage/NotFoundPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/research/inbox" replace />} />
      <Route element={<AppLayout />}>
        <Route path="/research/inbox" element={<InboxPage />} />
        <Route path="/research/search" element={<SearchPage />} />
        <Route path="/research/messages/:id" element={<DetailPage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}
