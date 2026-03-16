import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/auth'
import Layout from './components/Layout/Header'
import LoginPage from './pages/LoginPage'
import ChatPage from './pages/ChatPage'
import EditorPage from './pages/EditorPage'
import ProjectsPage from './pages/ProjectsPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  const { isAuthenticated, loading } = useAuthStore()

  if (loading) {
    return <div className="flex items-center justify-center h-screen">
      <div className="animate-spin text-4xl">⏳</div>
    </div>
  }

  return (
    <BrowserRouter>
      <Routes>
        {!isAuthenticated ? (
          <>
            <Route path="/login" element={<LoginPage />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </>
        ) : (
          <>
            <Route element={<Layout />}>
              <Route path="/" element={<ChatPage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/editor" element={<EditorPage />} />
              <Route path="/projects" element={<ProjectsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
          </>
        )}
      </Routes>
    </BrowserRouter>
  )
}

export default App