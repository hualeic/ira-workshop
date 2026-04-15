import axios from 'axios'
import { ERROR_MESSAGES } from '../constants'

const client = axios.create({
  baseURL: '/api/v1/research',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.data?.error) {
      const apiError = error.response.data.error
      return Promise.reject({
        code: apiError.code,
        message: ERROR_MESSAGES[apiError.code] || apiError.message,
        traceId: apiError.traceId,
        details: apiError.details || {},
        status: error.response.status,
      })
    }
    return Promise.reject({
      code: 'NETWORK_ERROR',
      message: '网络连接失败，请检查网络',
      traceId: null,
      status: 0,
    })
  }
)

export default client
