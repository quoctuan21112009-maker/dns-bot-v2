import { io, Socket } from 'socket.io-client'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class WebSocketService {
  private socket: Socket | null = null

  connect(url: string) {
    this.socket = io(API_BASE_URL, {
      path: url,
      auth: {
        token: localStorage.getItem('token'),
      },
    })

    this.socket.on('connect', () => {
      console.log('✅ WebSocket connected')
    })

    this.socket.on('disconnect', () => {
      console.log('❌ WebSocket disconnected')
    })

    return this.socket
  }

  emit(event: string, data: any) {
    this.socket?.emit(event, data)
  }

  on(event: string, callback: (data: any) => void) {
    this.socket?.on(event, callback)
  }

  disconnect() {
    this.socket?.disconnect()
  }
}

export const wsService = new WebSocketService()