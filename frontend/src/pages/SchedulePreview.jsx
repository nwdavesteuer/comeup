import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import './SchedulePreview.css'

const SchedulePreview = () => {
  const [schedule, setSchedule] = useState(null)
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [approving, setApproving] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    fetchSchedule()
  }, [])

  const fetchSchedule = async () => {
    try {
      const response = await api.get('/api/schedule/preview')
      setSchedule(response.data.schedule)
      setSummary(response.data.summary)
    } catch (error) {
      console.error('Failed to fetch schedule:', error)
      alert('Failed to load schedule. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async () => {
    setApproving(true)
    try {
      await api.post('/api/schedule/approve', { approved: true, modifications: [] })
      navigate('/dashboard')
    } catch (error) {
      console.error('Failed to approve schedule:', error)
      alert('Failed to approve schedule. Please try again.')
    } finally {
      setApproving(false)
    }
  }

  const handleModify = () => {
    // For MVP, just allow them to approve anyway
    // In future, this would open an editor
    alert('Schedule modification coming soon! For now, you can approve and edit later.')
  }

  if (loading) {
    return (
      <div className="schedule-preview-container">
        <div className="schedule-card">Loading your content schedule...</div>
      </div>
    )
  }

  if (!schedule || schedule.length === 0) {
    return (
      <div className="schedule-preview-container">
        <div className="schedule-card">
          <h2>No Schedule Generated</h2>
          <p>Unable to generate schedule. Please complete onboarding.</p>
        </div>
      </div>
    )
  }

  // Group schedule by day
  const scheduleByDay = {}
  schedule.forEach(item => {
    if (!scheduleByDay[item.day]) {
      scheduleByDay[item.day] = []
    }
    scheduleByDay[item.day].push(item)
  })

  return (
    <div className="schedule-preview-container">
      <div className="schedule-card">
        <h1>Your Content Schedule</h1>
        <p className="subtitle">Here's your personalized content plan for this week</p>

        {summary && (
          <div className="schedule-summary">
            <h3>Summary</h3>
            <div className="summary-stats">
              <div className="stat">
                <span className="stat-value">{summary.total_posts}</span>
                <span className="stat-label">Total Posts</span>
              </div>
              <div className="stat">
                <span className="stat-value">{summary.estimated_total_time}</span>
                <span className="stat-label">Estimated Time</span>
              </div>
            </div>
            {summary.posts_by_platform && (
              <div className="platform-breakdown">
                <strong>By Platform:</strong>
                {Object.entries(summary.posts_by_platform).map(([platform, count]) => (
                  <span key={platform} className="platform-tag">
                    {platform}: {count}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="schedule-content">
          <h3>This Week's Schedule</h3>
          {Object.entries(scheduleByDay).map(([day, items]) => (
            <div key={day} className="schedule-day">
              <h4>{day}</h4>
              {items.map((item, idx) => (
                <div key={idx} className="schedule-item">
                  <div className="item-header">
                    <span className="platform-badge">{item.platform}</span>
                    <span className="content-type-badge">{item.content_type}</span>
                    <span className="time-badge">{item.time_suggestion}</span>
                  </div>
                  <p className="item-idea">{item.idea}</p>
                  <p className="item-time">⏱️ {item.estimated_time}</p>
                </div>
              ))}
            </div>
          ))}
        </div>

        <div className="schedule-actions">
          <p className="approval-question">Does this schedule look good to you?</p>
          <div className="action-buttons">
            <button onClick={handleModify} className="btn-secondary">
              Make Changes
            </button>
            <button onClick={handleApprove} disabled={approving} className="btn-primary">
              {approving ? 'Creating Schedule...' : "Yes, This Looks Good!"}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SchedulePreview

