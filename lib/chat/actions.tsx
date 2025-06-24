'use server'

export type Message = {
  role: 'user' | 'assistant' | 'system' | 'function' | 'data' | 'tool'
  content: string
  id: string
  name?: string
}

export type AIState = {
  chatId: string
  messages: Message[]
}

export type UIState = {
  id: string
  display: React.ReactNode
}[]

// Simplified AI provider - not used but keeping to prevent build errors
export const AI = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>
}

// Stub function to prevent build errors
export const getUIStateFromAIState = (aiState: any) => {
  return []
}
 