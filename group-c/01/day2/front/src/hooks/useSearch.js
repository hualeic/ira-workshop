import { useCallback } from 'react'
import { useResearch } from '../context/ResearchContext'
import { searchMessages } from '../api/researchApi'
import { useErrorHandler } from './useErrorHandler'
import { PAGE_LIMIT } from '../constants'

export function useSearch() {
  const { state, dispatch } = useResearch()
  const { handleError } = useErrorHandler()
  const { search } = state

  const doSearch = useCallback(
    async (query, dateRange = {}) => {
      if (!query || query.trim().length === 0) return
      dispatch({ type: 'SEARCH_START', payload: { query: query.trim() } })
      try {
        const data = await searchMessages({
          q: query.trim(),
          from: dateRange.from,
          to: dateRange.to,
          limit: PAGE_LIMIT,
        })
        dispatch({ type: 'SEARCH_LOADED', payload: data, append: false })
      } catch (err) {
        dispatch({ type: 'SEARCH_ERROR', payload: err })
        handleError(err)
      }
    },
    [dispatch, handleError]
  )

  const loadMore = useCallback(async () => {
    if (!search.nextCursor || search.isSearching) return
    try {
      const data = await searchMessages({
        q: search.query,
        cursor: search.nextCursor,
        limit: PAGE_LIMIT,
      })
      dispatch({ type: 'SEARCH_LOADED', payload: data, append: true })
    } catch (err) {
      handleError(err)
    }
  }, [search.nextCursor, search.isSearching, search.query, dispatch, handleError])

  return { ...search, search: doSearch, loadMore }
}
