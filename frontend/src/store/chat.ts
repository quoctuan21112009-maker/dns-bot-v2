import { create } from 'zustand'
import { Message, ChatSession } from '../types'

interface ChatState {
  messages: Message[]
  sessions: ChatSession[]
  currentSession: ChatSession | null
  isLoading: boolean
  addMessage: (message: Message) => void
  setMessages: (messages: Message[]) => void
  setCurrentSession: (session: ChatSession) => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  sessions: [],
  currentSession: null,
  isLoading: false,

  addMessage: (message: Message) => set((state) => ({
    messages: [...state.messages, message]
  })),

  setMessages: (messages: Message[]) => set({ messages }),

  setCurrentSession: (session: ChatSession) => set({ 
    currentSession: session,
    messages: []
  })
}))