import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../services/api'
import './Dashboard.css'

const Dashboard = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [onboardingComplete, setOnboardingComplete] = useState(false)
  const [connections, setConnections] = useState([])
  const [schedule, setSchedule] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkOnboardingStatus()
    fetchConnections()
    fetchSchedule()
  }, [])

  const checkOnboardingStatus = async () => {
    try {
      const response = await api.get('/api/onboarding/status')
      if (!response.data.is_complete) {
        navigate('/onboarding')
      } else {
        setOnboardingComplete(true)
      }
    } catch (error) {
      console.error('Failed to check onboarding status:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchConnections = async () => {
    try {
      const response = await api.get('/api/connections')
      setConnections(response.data.connections || [])
    } catch (error) {
      console.error('Failed to fetch connections:', error)
    }
  }

  const fetchSchedule = async () => {
    try {
      const response = await api.get('/api/schedule/this-week')
      setSchedule(response.data)
    } catch (error) {
      console.error('Failed to fetch schedule:', error)
    }
  }

  const handleConnect = async (platform) => {
    try {
      const response = await api.get(`/api/connect/${platform}`)
      // Open OAuth URL in the same window
      window.location.href = response.data.auth_url
    } catch (error) {
      console.error(`Failed to connect ${platform}:`, error)
      if (error.response?.status === 500 && error.response?.data?.detail?.includes('client_id')) {
        alert(`OAuth is not configured for ${platform}. The app works great without connections! If you'd like to set up OAuth, see OAUTH_SETUP.md for instructions.`)
      } else {
        alert(`Failed to connect ${platform}. The app works great without connections! If you'd like to set up OAuth, see OAUTH_SETUP.md for instructions.`)
      }
    }
  }

  const isConnected = (platform) => {
    return connections.some(conn => conn.platform === platform && conn.is_active)
  }

  if (loading || !onboardingComplete) {
    return <div className="dashboard-container">Loading...</div>
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>ComeUp</h1>
        <div className="user-info">
          <span>Welcome, {user?.email}</span>
          <button onClick={logout} className="btn-secondary">
            Logout
          </button>
        </div>
      </header>
      <main className="dashboard-main">
        <div className="dashboard-card">
          <h2>Welcome to ComeUp!</h2>
          <p>Your content schedule is ready! Connect your accounts (optional) to get even more personalized recommendations:</p>
          <div className="connection-buttons">
            <button 
              className={`btn-primary ${isConnected('spotify') ? 'connected' : ''}`}
              onClick={() => handleConnect('spotify')}
              disabled={isConnected('spotify')}
            >
              {isConnected('spotify') ? '✓ Spotify Connected' : 'Connect Spotify (Optional)'}
            </button>
            <button 
              className={`btn-primary ${isConnected('instagram') ? 'connected' : ''}`}
              onClick={() => handleConnect('instagram')}
              disabled={isConnected('instagram')}
            >
              {isConnected('instagram') ? '✓ Instagram Connected' : 'Connect Instagram (Optional)'}
            </button>
          </div>
          {connections.length > 0 && (
            <p style={{ marginTop: '16px', color: '#666', fontSize: '14px' }}>
              Connected: {connections.map(c => c.platform).join(', ')}
            </p>
          )}
          <p style={{ marginTop: '16px', color: '#999', fontSize: '13px', fontStyle: 'italic' }}>
            Note: Your content schedule works great without connections! Connecting accounts helps us provide more personalized insights based on your actual performance data.
          </p>
        </div>

        {schedule && schedule.schedule && schedule.schedule.length > 0 && (
          <div className="dashboard-card" style={{ marginTop: '24px' }}>
            <h2>This Week's Content Schedule</h2>
            <div className="schedule-preview">
              {schedule.schedule.slice(0, 3).map((item, idx) => (
                <div key={idx} className="schedule-item-preview">
                  <div className="item-header">
                    <span className="platform-badge">{item.platform}</span>
                    <span className="day-badge">{item.day}</span>
                  </div>
                  <p className="item-idea">{item.idea}</p>
                  <p className="item-time">⏱️ {item.time_suggestion}</p>
                </div>
              ))}
              {schedule.schedule.length > 3 && (
                <p style={{ marginTop: '16px', textAlign: 'center' }}>
                  <button 
                    onClick={() => navigate('/schedule-preview')}
                    className="btn-secondary"
                  >
                    View Full Schedule ({schedule.schedule.length} posts)
                  </button>
                </p>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default Dashboard

