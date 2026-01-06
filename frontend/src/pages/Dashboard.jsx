import { useAuth } from '../contexts/AuthContext'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../services/api'
import './Dashboard.css'

const Dashboard = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  const [onboardingComplete, setOnboardingComplete] = useState(false)
  const [connections, setConnections] = useState([])
  const [schedule, setSchedule] = useState(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    checkOnboardingStatus()
    fetchConnections()
    fetchSchedule()
    
    // Check for OAuth callback messages
    const connected = searchParams.get('connected')
    const errorParam = searchParams.get('error')
    const messageParam = searchParams.get('message')
    const platform = searchParams.get('platform')
    
    if (connected) {
      setMessage(messageParam || `${connected} connected successfully!`)
      // Clear URL params
      setSearchParams({})
      // Refresh connections
      fetchConnections()
    }
    
    if (errorParam) {
      setError(`Failed to connect ${platform || 'platform'}: ${errorParam}`)
      setSearchParams({})
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
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

  const hasRequiredConnections = () => {
    return isConnected('spotify') && isConnected('instagram')
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
        {message && (
          <div className="dashboard-card" style={{ backgroundColor: '#d4edda', borderColor: '#c3e6cb', marginBottom: '16px' }}>
            <p style={{ color: '#155724', margin: 0 }}>{message}</p>
          </div>
        )}
        {error && (
          <div className="dashboard-card" style={{ backgroundColor: '#f8d7da', borderColor: '#f5c6cb', marginBottom: '16px' }}>
            <p style={{ color: '#721c24', margin: 0 }}>{error}</p>
          </div>
        )}
        <div className="dashboard-card">
          <h2>Welcome to ComeUp!</h2>
          {!hasRequiredConnections() && (
            <div style={{ backgroundColor: '#fff3cd', border: '1px solid #ffc107', padding: '12px', borderRadius: '4px', marginBottom: '16px' }}>
              <p style={{ color: '#856404', margin: 0, fontWeight: 'bold' }}>
                ⚠️ Required: Please connect both Spotify and Instagram accounts to continue.
              </p>
            </div>
          )}
          <p>Connect your accounts to get personalized content recommendations and insights:</p>
          <div className="connection-buttons">
            <button 
              className={`btn-primary ${isConnected('spotify') ? 'connected' : ''}`}
              onClick={() => handleConnect('spotify')}
              disabled={isConnected('spotify')}
            >
              {isConnected('spotify') ? '✓ Spotify Connected' : 'Connect Spotify (Required)'}
            </button>
            <button 
              className={`btn-primary ${isConnected('instagram') ? 'connected' : ''}`}
              onClick={() => handleConnect('instagram')}
              disabled={isConnected('instagram')}
            >
              {isConnected('instagram') ? '✓ Instagram Connected' : 'Connect Instagram (Required)'}
            </button>
          </div>
          {connections.length > 0 && (
            <p style={{ marginTop: '16px', color: '#666', fontSize: '14px' }}>
              Connected: {connections.map(c => c.platform).join(', ')}
            </p>
          )}
          {hasRequiredConnections() && (
            <p style={{ marginTop: '16px', color: '#28a745', fontSize: '14px', fontWeight: 'bold' }}>
              ✓ All required accounts connected! You can now access your content schedule.
            </p>
          )}
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

