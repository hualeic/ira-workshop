import client from './client'

export async function checkHealth() {
  const { data } = await client.get('/health')
  return data
}

export async function fetchMessages({ cursor, limit = 20, unreadOnly = false, category } = {}) {
  const params = { limit }
  if (cursor) params.cursor = cursor
  if (unreadOnly) params.unreadOnly = 'true'
  if (category) params.category = category
  const { data } = await client.get('/messages', { params })
  return data
}

export async function searchMessages({ q, from, to, cursor, limit = 20 } = {}) {
  const params = { q, limit }
  if (from) params.from = from
  if (to) params.to = to
  if (cursor) params.cursor = cursor
  const { data } = await client.get('/messages/search', { params })
  return data
}

export async function fetchMessageDetail(messageId) {
  const { data } = await client.get(`/messages/${messageId}`)
  return data
}

export async function markAsRead(messageId) {
  const { data } = await client.patch(`/messages/${messageId}/read`, { read: true })
  return data
}
