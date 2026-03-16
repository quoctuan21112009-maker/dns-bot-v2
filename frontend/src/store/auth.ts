import { create } from 'zustand'
import { User } from '../types'
import api from '../services/api'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (data: any) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: true,

  login: async (username: string, password: string) => {
    try {
      const response = await api.post('/api/auth/login', { username, password })
      const { access_token, user } = response.data
      
      localStorage.setItem('token', access_token)
      set({ user, token: access_token, isAuthenticated: true })
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  },

  register: async (data: any) => {
    try {
      await api.post('/api/auth/register', data)
    } catch (error) {
      console.error('Register failed:', error)
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, token: null, isAuthenticated: false })
  },

  checkAuth: async () => {
    try {
      const response = await api.get('/api/auth/me')
      set({ user: response.data, isAuthenticated: true, loading: false })
    } catch {
      set({ isAuthenticated: false, loading: false })
    }
  }
}))