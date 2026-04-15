import { useEffect, useCallback } from 'react'
import { useResearch } from '../context/ResearchContext'
import { fetchMessages } from '../api/researchApi'
import { useErrorHandler } from './useErrorHandler'
import { PAGE_LIMIT } from '../constants'

export function useMessages() {
  const { state, dispatch } = useResearch()
  const { handleError } = useErrorHandler()
  const { messages, filters } = state

  const load = useCallback(
    async (cursor = null, append = false) => {
      dispatch({ type: 'MESSAGES_LOADING' })
      try {
        const data = await fetchMessages({
          cursor,
          limit: PAGE_LIMIT,
          unreadOnly: filters.unreadOnly,
          category: filters.category,
        })
        dispatch({ type: 'MESSAGES_LOADED', payload: data, append })
      } catch (err) {
        dispatch({ type: 'MESSAGES_ERROR', payload: err })
        handleError(err)
      }
    },
    [dispatch, filters, handleError]
  )

  useEffect(() => {
    load()
  }, [filters.unreadOnly, filters.category]) // eslint-disable-line react-hooks/exhaustive-deps

  const loadMore = useCallback(() => {
    if (messages.nextCursor && !messages.isLoading) {
      load(messages.nextCursor, true)
    }
  }, [messages.nextCursor, messages.isLoading, load])

  const refresh = useCallback(() => load(), [load])

  return { ...messages, loadMore, refresh }
}
