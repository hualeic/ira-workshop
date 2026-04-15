import { createContext, useContext, useReducer } from 'react'
import { researchReducer, initialState } from './researchReducer'

const ResearchContext = createContext(null)

export function ResearchProvider({ children }) {
  const [state, dispatch] = useReducer(researchReducer, initialState)
  return (
    <ResearchContext.Provider value={{ state, dispatch }}>
      {children}
    </ResearchContext.Provider>
  )
}

export function useResearch() {
  const ctx = useContext(ResearchContext)
  if (!ctx) throw new Error('useResearch must be used within ResearchProvider')
  return ctx
}
