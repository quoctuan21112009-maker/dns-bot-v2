import { Outlet, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/auth'

export default function Layout() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex h-screen bg-slate-900">
      {/* Sidebar */}
      <div className="w-64 bg-slate-800 border-r border-slate-700 p-4">
        <div className="flex items-center gap-2 mb-8">
          <div className="text-2xl">🤖</div>
          <span className="font-bold text-white">DNS Bot</span>
        </div>

        <nav className="space-y-2">
          {[
            { path: '/', icon: '💬', label: 'Chat' },
            { path: '/editor', icon: '💻', label: 'Code Editor' },
            { path: '/projects', icon: '📁', label: 'Projects' },
            { path: '/settings', icon: '⚙️', label: 'Settings' },
          ].map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className="w-full text-left px-4 py-2 rounded-lg hover:bg-slate-700 text-slate-300 transition-colors"
            >
              {item.icon} {item.label}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-4 left-4 right-4">
          <div className="bg-slate-700 rounded-lg p-3 mb-3">
            <p className="text-sm text-slate-300">👤 {user?.fullname || user?.username}</p>
            <p className="text-xs text-slate-400">{user?.role}</p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 bg-red-600 rounded-lg text-white hover:bg-red-700 transition-colors"
          >
            🚪 Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  )
}