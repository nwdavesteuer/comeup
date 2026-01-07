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

  // Group schedule by date and activity type
  const scheduleByDate = {}
  schedule.forEach(item => {
    const date = item.date
    if (!scheduleByDate[date]) {
      scheduleByDate[date] = { filming: [], editing: [], posting: [] }
    }
    if (item.activity_type === 'filming') {
      scheduleByDate[date].filming.push(item)
    } else if (item.activity_type === 'editing') {
      scheduleByDate[date].editing.push(item)
    } else if (item.activity_type === 'posting') {
      scheduleByDate[date].posting.push(item)
    }
  })

  // Sort dates
  const sortedDates = Object.keys(scheduleByDate).sort()

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
  }

  return (
    <div className="schedule-preview-container">
      <div className="schedule-card">
        <h1>Your Content Schedule</h1>
        <p className="subtitle">Here's your personalized content plan with detailed instructions</p>

        <div className="schedule-content">
          {sortedDates.map((date) => {
            const daySchedule = scheduleByDate[date]
            const hasContent = daySchedule.filming.length > 0 || daySchedule.editing.length > 0 || daySchedule.posting.length > 0
            
            if (!hasContent) return null

            return (
              <div key={date} className="schedule-day">
                <h4>{formatDate(date)}</h4>
                
                {/* Filming Activities */}
                {daySchedule.filming.map((item, idx) => (
                  <div key={`filming-${idx}`} className="schedule-item filming">
                    <div className="item-header">
                      <span className="activity-badge filming">📹 Filming</span>
                      <span className="platform-badge">{item.platform}</span>
                      <span className="format-badge">{item.format}</span>
                    </div>
                    <h5 className="content-name">{item.content_name}</h5>
                    
                    {item.visual_direction && (
                      <div className="visual-direction">
                        <strong>Visual Direction:</strong>
                        <p><strong>Color Palette:</strong> {item.visual_direction.color_palette}</p>
                        <p><strong>Style:</strong> {item.visual_direction.style_description}</p>
                      </div>
                    )}
                    
                    {item.content_description && (
                      <div className="content-description">
                        <strong>Content Description:</strong>
                        <p>{item.content_description}</p>
                      </div>
                    )}
                    
                    {item.shot_list && item.shot_list.length > 0 && (
                      <div className="shot-list">
                        <strong>Shot List:</strong>
                        <ul>
                          {item.shot_list.map((shot, shotIdx) => (
                            <li key={shotIdx}>
                              <strong>{shot.shot}</strong> ({shot.time_range}): {shot.description}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    <div className="time-info">
                      <p><strong>Setup Time:</strong> {item.setup_time}</p>
                      <p><strong>Filming Duration:</strong> {item.filming_duration}</p>
                    </div>
                  </div>
                ))}

                {/* Editing Activities */}
                {daySchedule.editing.map((item, idx) => (
                  <div key={`editing-${idx}`} className="schedule-item editing">
                    <div className="item-header">
                      <span className="activity-badge editing">✂️ Editing</span>
                      <span className="platform-badge">{item.platform}</span>
                      <span className="format-badge">{item.format}</span>
                    </div>
                    <h5 className="content-name">{item.content_name}</h5>
                    <p><strong>Editing Duration:</strong> {item.editing_duration}</p>
                  </div>
                ))}

                {/* Posting Activities */}
                {daySchedule.posting.map((item, idx) => (
                  <div key={`posting-${idx}`} className="schedule-item posting">
                    <div className="item-header">
                      <span className="activity-badge posting">📤 Posting</span>
                      <span className="platform-badge">{item.platform}</span>
                      <span className="format-badge">{item.format}</span>
                    </div>
                    <h5 className="content-name">{item.content_name}</h5>
                    <p><strong>Posting Time:</strong> {item.posting_time}</p>
                    
                    {item.caption && (
                      <div className="caption">
                        <strong>Caption:</strong>
                        <p>{item.caption}</p>
                      </div>
                    )}
                    
                    {item.hashtags && item.hashtags.length > 0 && (
                      <div className="hashtags">
                        <strong>Hashtags:</strong>
                        <p>{item.hashtags.map(tag => `#${tag}`).join(' ')}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )
          })}
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

