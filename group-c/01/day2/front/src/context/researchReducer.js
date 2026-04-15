export const initialState = {
  messages: { items: [], nextCursor: null, hasMore: true, isLoading: false, error: null },
  search: { items: [], nextCursor: null, hasMore: false, isSearching: false, query: '', error: null },
  detail: { message: null, isLoading: false, error: null },
  filters: { unreadOnly: false, category: null },
}

export function researchReducer(state, action) {
  switch (action.type) {
    case 'MESSAGES_LOADING':
      return { ...state, messages: { ...state.messages, isLoading: true, error: null } }
    case 'MESSAGES_LOADED': {
      const append = action.append
      const items = append ? [...state.messages.items, ...action.payload.items] : action.payload.items
      return {
        ...state,
        messages: {
          items,
          nextCursor: action.payload.nextCursor,
          hasMore: action.payload.hasMore,
          isLoading: false,
          error: null,
        },
      }
    }
    case 'MESSAGES_ERROR':
      return { ...state, messages: { ...state.messages, isLoading: false, error: action.payload } }
    case 'MESSAGES_RESET':
      return { ...state, messages: { ...initialState.messages } }
    case 'SET_FILTERS':
      return {
        ...state,
        filters: { ...state.filters, ...action.payload },
        messages: { ...initialState.messages },
      }

    case 'SEARCH_START':
      return {
        ...state,
        search: { ...initialState.search, isSearching: true, query: action.payload.query },
      }
    case 'SEARCH_LOADED': {
      const append = action.append
      const items = append ? [...state.search.items, ...action.payload.items] : action.payload.items
      return {
        ...state,
        search: {
          ...state.search,
          items,
          nextCursor: action.payload.nextCursor,
          hasMore: action.payload.hasMore,
          isSearching: false,
          error: null,
        },
      }
    }
    case 'SEARCH_ERROR':
      return { ...state, search: { ...state.search, isSearching: false, error: action.payload } }

    case 'DETAIL_LOADING':
      return { ...state, detail: { message: null, isLoading: true, error: null } }
    case 'DETAIL_LOADED':
      return { ...state, detail: { message: action.payload, isLoading: false, error: null } }
    case 'DETAIL_ERROR':
      return { ...state, detail: { message: null, isLoading: false, error: action.payload } }

    case 'MARK_READ_OPTIMISTIC': {
      const id = action.payload
      const updateRead = (items) =>
        items.map((item) => (item.messageId === id ? { ...item, read: true } : item))
      return {
        ...state,
        messages: { ...state.messages, items: updateRead(state.messages.items) },
        search: { ...state.search, items: updateRead(state.search.items) },
        detail:
          state.detail.message?.messageId === id
            ? { ...state.detail, message: { ...state.detail.message, read: true } }
            : state.detail,
      }
    }
    case 'MARK_READ_ROLLBACK': {
      const id = action.payload
      const revert = (items) =>
        items.map((item) => (item.messageId === id ? { ...item, read: false } : item))
      return {
        ...state,
        messages: { ...state.messages, items: revert(state.messages.items) },
        search: { ...state.search, items: revert(state.search.items) },
        detail:
          state.detail.message?.messageId === id
            ? { ...state.detail, message: { ...state.detail.message, read: false } }
            : state.detail,
      }
    }

    default:
      return state
  }
}
