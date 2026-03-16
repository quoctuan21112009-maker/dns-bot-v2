export interface User {
  id: number
  username: string
  email?: string
  fullname?: string
  role: 'student' | 'teacher' | 'admin'
  ai_provider: string
  ai_model: string
}

export interface Message {
  id: number
  user_id: number
  session_id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  file_id?: string
  created_at: string
}

export interface Task {
  id: number
  user_id: number
  title: string
  description?: string
  status: 'todo' | 'in_progress' | 'review' | 'done'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  due_date?: string
  created_at: string
}

export interface ChatSession {
  id: string
  user_id: number
  title: string
  created_at: string
}

export interface CodeRunResult {
  output: string
  error: string
  elapsed_time: number
  status: string
}