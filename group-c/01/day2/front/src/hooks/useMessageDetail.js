import { useEffect, useCallback } from 'react'
import { useResearch } from '../context/ResearchContext'
import { fetchMessageDetail, markAsRead } from '../api/researchApi'
import { useErrorHandler } from './useErrorHandler'

export function useMessageDetail(messageId) {
  const { state, dispatch } = useResearch()
  const { handleError } = useErrorHandler()
  const { detail } = state

  useEffect(() => {
    if (!messageId) return
    let cancelled = false
    dispatch({ type: 'DETAIL_LOADING' })
    fetchMessageDetail(messageId)
      .then((data) => {
        if (!cancelled) dispatch({ type: 'DETAIL_LOADED', payload: data })
      })
      .catch((err) => {
        if (!cancelled) {
          dispatch({ type: 'DETAIL_ERROR', payload: err })
          handleError(err)
        }
      })
    return () => { cancelled = true }
  }, [messageId]) // eslint-disable-line react-hooks/exhaustive-deps

  const doMarkRead = useCallback(async () => {
    if (!messageId) return
    dispatch({ type: 'MARK_READ_OPTIMISTIC', payload: messageId })
    try {
      await markAsRead(messageId)
    } catch (err) {
      dispatch({ type: 'MARK_READ_ROLLBACK', payload: messageId })
      handleError(err)
    }
  }, [messageId, dispatch, handleError])

  return { ...detail, markAsRead: doMarkRead }
}
