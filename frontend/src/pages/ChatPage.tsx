import { useEffect, useState } from 'react'
import { useChatStore } from '../store/chat'
import { useAuthStore } from '../store/auth'
import api from '../services/api'

export default function ChatPage() {
  const [messageText, setMessageText] = useState('')
  const messages = useChatStore((state) => state.messages)
  const addMessage = useChatStore((state) => state.addMessage)
  const user = useAuthStore((state) => state.user)
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async () => {
    if (!messageText.trim()) return

    setIsLoading(true)
    try {
      const response = await api.post('/api/chat/send', {
        message: messageText,
        session_id: `session_${user?.id}`,
      })

      // Add user message
      addMessage({
        id: Date.now(),
        user_id: user!.id,
        session_id: `session_${user?.id}`,
        role: 'user',
        content: messageText,
        created_at: new Date().toISOString(),
      })

      // Add AI response
      addMessage({
        id: Date.now() + 1,
        user_id: user!.id,
        session_id: `session_${user?.id}`,
        role: 'assistant',
        content: response.data.reply,
        created_at: new Date().toISOString(),
      })

      setMessageText('')
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full bg-slate-900">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-slate-400">
            <div className="text-center">
              <div className="text-6xl mb-4">🤖</div>
              <p>Start chatting with DNS Bot!</p>
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-4 ${
                msg.role === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              <div className="text-2xl">{msg.role === 'user' ? '👤' : '🤖'}</div>
              <div
                className={`max-w-md p-4 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-purple-600 text-white'
                    : 'bg-slate-800 text-slate-100'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="p-6 border-t border-slate-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={messageText}
            onChange={(e) => setMessageText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-purple-500"
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading}
            className="px-6 py-2 bg-purple-600 rounded-lg text-white hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </div>
      </div>
    </div>
  )
}