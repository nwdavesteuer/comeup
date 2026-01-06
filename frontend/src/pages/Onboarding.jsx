import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import './Onboarding.css'

const Onboarding = () => {
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [answer, setAnswer] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchStatus()
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await api.get('/api/onboarding/status')
      setProgress(response.data.progress)
      setCurrentQuestion(response.data.current_question)
      if (response.data.is_complete) {
        navigate('/dashboard')
      }
    } catch (error) {
      console.error('Failed to fetch onboarding status:', error)
      if (error.response?.status === 401) {
        // Not authenticated, redirect to login
        navigate('/login')
      } else {
        // Show error message
        alert('Failed to load onboarding. Please refresh the page.')
      }
    } finally {
      setLoading(false)
    }
  }

  const saveAnswer = async (questionKey, answerValue) => {
    setSaving(true)
    try {
      await api.post('/api/onboarding/answer', {
        question_key: questionKey,
        answer: answerValue,
      })
      await fetchStatus()
      setAnswer(null)
    } catch (error) {
      console.error('Failed to save answer:', error)
      alert('Failed to save answer. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  const handleAnswer = (value) => {
    setAnswer(value)
  }

  const handleNext = () => {
    if (answer === null) return
    saveAnswer(currentQuestion, answer)
  }

  const handleComplete = async () => {
    try {
      await api.post('/api/onboarding/complete')
      navigate('/schedule-preview')
    } catch (error) {
      alert('Failed to complete onboarding. Please try again.')
    }
  }

  if (loading) {
    return (
      <div className="onboarding-container">
        <div className="onboarding-card">
          <h2>Loading...</h2>
          <p>Setting up your onboarding experience...</p>
        </div>
      </div>
    )
  }

  const questionComponents = {
    content_time: (
      <Question
        title="Content Creation Time"
        description="How many hours per week can you dedicate to creating content?"
        note="Artists posting 3-5 times per week typically see the best engagement, which usually requires 5-10 hours/week."
        options={[
          { value: 'less_than_2', label: 'Less than 2 hours' },
          { value: '2_5', label: '2-5 hours' },
          { value: '5_10', label: '5-10 hours' },
          { value: '10_15', label: '10-15 hours' },
          { value: 'more_than_15', label: 'More than 15 hours' },
        ]}
        answer={answer}
        onAnswer={handleAnswer}
      />
    ),
    live_performances: (
      <Question
        title="Live Performances"
        description="Do you perform live shows (concerts, open mics, gigs)?"
        note="Live performance content (behind-the-scenes, clips, audience reactions) often drives strong engagement and can convert viewers to Spotify listeners."
        options={[
          { value: 'regularly', label: 'Yes, regularly (monthly or more)' },
          { value: 'occasionally', label: 'Yes, occasionally (a few times per year)' },
          { value: 'planning', label: 'Not yet, but I plan to' },
          { value: 'no', label: 'No, I focus on recorded music' },
        ]}
        answer={answer}
        onAnswer={handleAnswer}
      />
    ),
    content_types: (
      <Question
        title="Content Types"
        description="What types of content do you enjoy creating? (Select all that apply)"
        note="Behind-the-scenes and music snippets typically drive the most engagement and Spotify clicks. If you select 'All of the above,' I'll focus on the highest-performing types."
        options={[
          { value: 'behind_scenes', label: 'Behind-the-scenes (studio, writing process)' },
          { value: 'music_snippets', label: 'Music snippets/previews (song clips, hooks)' },
          { value: 'performance', label: 'Performance videos (acoustic versions, covers)' },
          { value: 'lifestyle', label: 'Lifestyle/personal (day-in-the-life, personality)' },
          { value: 'educational', label: 'Educational/tips (production tips, industry advice)' },
          { value: 'trends', label: 'Trend participation (dancing, challenges, viral formats)' },
          { value: 'storytelling', label: 'Storytelling (song meanings, personal stories)' },
          { value: 'all', label: "All of the above (I'll optimize for maximum engagement)" },
        ]}
        answer={answer}
        onAnswer={handleAnswer}
        multiple={true}
      />
    ),
    music_inspiration: (
      <MusicInspirationQuestion
        answer={answer}
        onAnswer={handleAnswer}
      />
    ),
    visual_style: (
      <VisualStyleQuestion
        answer={answer}
        onAnswer={handleAnswer}
      />
    ),
    challenges: (
      <Question
        title="Top Challenges"
        description="What are your top 3 challenges with content creation? (Select up to 3)"
        note="Most artists struggle with consistency and idea generation. I'll help with both—providing content ideas tailored to your style and creating a schedule that fits your available time."
        options={[
          { value: 'ideas', label: 'Coming up with ideas (I don\'t know what to post)' },
          { value: 'time', label: 'Finding time to create (I have ideas but struggle to execute)' },
          { value: 'consistency', label: 'Consistency (I post sporadically, not regularly)' },
          { value: 'engagement', label: 'Engagement (My posts don\'t get much interaction)' },
          { value: 'quality', label: 'Quality/production (I want my content to look more professional)' },
          { value: 'conversion', label: 'Converting followers to Spotify listeners (People follow but don\'t stream)' },
          { value: 'starting', label: "I'm just getting started (Haven't created much content yet)" },
          { value: 'other', label: "Other (I'll describe it)" },
        ]}
        answer={answer}
        onAnswer={handleAnswer}
        multiple={true}
        maxSelections={3}
      />
    ),
    whats_working: (
      <Question
        title="What's Working"
        description="What's currently working well for you? (Select all that apply)"
        note="Understanding what already works helps me recommend similar content that's likely to perform well for you. If nothing is working, I'll recommend the highest-performing content types based on your style and goals."
        options={[
          { value: 'behind_scenes', label: 'Behind-the-scenes content (People love seeing my process)' },
          { value: 'music_snippets', label: 'Music snippets (Song previews get good engagement)' },
          { value: 'live', label: 'Live performances (Acoustic or live videos perform well)' },
          { value: 'lifestyle', label: 'Personal/lifestyle content (Day-in-the-life posts resonate)' },
          { value: 'trends', label: 'Trend participation (Jumping on trends gets views)' },
          { value: 'storytelling', label: 'Storytelling (Sharing my journey connects with people)' },
          { value: 'starting', label: "Nothing specific yet / I'm just starting out" },
          { value: 'nothing', label: 'None of my content is working well for me' },
        ]}
        answer={answer}
        onAnswer={handleAnswer}
        multiple={true}
      />
    ),
    upcoming_music: (
      <UpcomingMusicQuestion
        answer={answer}
        onAnswer={handleAnswer}
      />
    ),
    collaborations: (
      <Question
        title="Collaborations"
        description="Do you plan on releasing any songs with other artists?"
        note="Collaboration releases can expand your reach and introduce you to new audiences. Cross-promotion content often performs well and can drive streams for both artists."
        options={[
          { value: 'coming_up', label: 'Yes, I have collaborations coming up' },
          { value: 'open', label: "Yes, I'm open to it but nothing planned yet" },
          { value: 'maybe', label: 'Not sure / Maybe in the future' },
          { value: 'no', label: 'No, I prefer to release solo music' },
        ]}
        answer={answer}
        onAnswer={handleAnswer}
      />
    ),
    upcoming_content: (
      <UpcomingContentQuestion
        answer={answer}
        onAnswer={handleAnswer}
      />
    ),
  }

  const questionComponent = questionComponents[currentQuestion]

  if (!currentQuestion) {
    return (
      <div className="onboarding-container">
        <div className="onboarding-card">
          <h1>Onboarding Complete!</h1>
          <p>You've answered all the questions. Ready to connect your accounts?</p>
          <button onClick={handleComplete} className="btn-primary">
            Complete Onboarding
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="onboarding-container">
      <div className="onboarding-card">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${(progress / 10) * 100}%` }}></div>
        </div>
        <p className="progress-text">Question {progress + 1} of 10</p>
        
        {questionComponent}

        <div className="button-group">
          <button
            onClick={handleNext}
            disabled={answer === null || saving}
            className="btn-primary"
          >
            {saving ? 'Saving...' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  )
}

// Question component for multiple choice
const Question = ({ title, description, note, options, answer, onAnswer, multiple = false, maxSelections = null }) => {
  const handleSelect = (value) => {
    if (multiple) {
      const current = Array.isArray(answer) ? answer : []
      if (current.includes(value)) {
        onAnswer(current.filter(v => v !== value))
      } else {
        if (maxSelections && current.length >= maxSelections) {
          return // Don't add more if max reached
        }
        onAnswer([...current, value])
      }
    } else {
      onAnswer(value)
    }
  }

  const isSelected = (value) => {
    if (multiple) {
      return Array.isArray(answer) && answer.includes(value)
    }
    return answer === value
  }

  return (
    <div className="question">
      <h2>{title}</h2>
      <p className="description">{description}</p>
      {note && <p className="note">{note}</p>}
      <div className="options">
        {options.map((option) => (
          <button
            key={option.value}
            onClick={() => handleSelect(option.value)}
            className={`option ${isSelected(option.value) ? 'selected' : ''}`}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  )
}

// Music inspiration question (text input)
const MusicInspirationQuestion = ({ answer, onAnswer }) => {
  const [text, setText] = useState(answer || '')
  const [showGenre, setShowGenre] = useState(false)

  useEffect(() => {
    if (text.toLowerCase().includes('not sure') || text.toLowerCase().includes("i'm not sure")) {
      setShowGenre(true)
    }
  }, [text])

  const handleSubmit = () => {
    if (showGenre) {
      // Will be handled by genre input
      return
    }
    onAnswer(text)
  }

  if (showGenre) {
    return (
      <div className="question">
        <h2>Music Inspiration</h2>
        <p className="description">What genre does your music fit into?</p>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="e.g., Indie Pop, Hip-Hop, Rock"
          className="text-input"
          onBlur={() => onAnswer({ genre: text })}
        />
      </div>
    )
  }

  return (
    <div className="question">
      <h2>Music Inspiration</h2>
      <p className="description">
        Name 2-3 artists that inspire your music creation. This helps me understand your sound and recommend content that resonates with your audience.
      </p>
      <p className="note">If you're not sure, I can help narrow it down.</p>
      <input
        type="text"
        value={text}
        onChange={(e) => {
          setText(e.target.value)
          onAnswer(e.target.value)
        }}
        placeholder="e.g., Dominic Fike, Bon Iver, The Beatles"
        className="text-input"
      />
    </div>
  )
}

// Visual style question with follow-up
const VisualStyleQuestion = ({ answer, onAnswer }) => {
  const [showFollowup, setShowFollowup] = useState(false)
  const [followupAnswer, setFollowupAnswer] = useState({})

  const options = [
    { value: 'natural', label: 'Natural/outdoor (forests, beaches, golden hour, earth tones)' },
    { value: 'vintage', label: 'Vintage/retro with film grain (warm tones, sepia, nostalgic)' },
    { value: 'moody', label: 'Moody/atmospheric (low light, shadows, blues and purples)' },
    { value: 'minimalist', label: 'Minimalist/clean (white/neutral backgrounds, simple compositions)' },
    { value: 'urban', label: 'Urban/street (cityscapes, concrete, neon accents)' },
    { value: 'studio', label: 'Studio/indoor intimate (cozy spaces, warm lighting, close-ups)' },
    { value: 'not_sure', label: "I'm not sure / help me narrow it down" },
  ]

  const handleSelect = (value) => {
    if (value === 'not_sure') {
      setShowFollowup(true)
      onAnswer({ type: 'not_sure' })
    } else {
      const current = Array.isArray(answer) ? answer : []
      if (current.includes(value)) {
        onAnswer(current.filter(v => v !== value))
      } else {
        onAnswer([...current, value])
      }
    }
  }

  if (showFollowup) {
    return (
      <div className="question">
        <h2>Visual Style - Help Narrow Down</h2>
        <p className="description">Where do you typically create or film your content?</p>
        <div className="options">
          {['outdoors', 'indoors', 'both', 'not_started'].map((opt) => (
            <button
              key={opt}
              onClick={() => setFollowupAnswer({ ...followupAnswer, location: opt })}
              className={`option ${followupAnswer.location === opt ? 'selected' : ''}`}
            >
              {opt === 'outdoors' ? 'Outdoors (parks, nature, streets, beaches)' :
               opt === 'indoors' ? 'Indoors (home, studio, bedroom, kitchen)' :
               opt === 'both' ? 'Mix of both' :
               "I haven't started creating content yet"}
            </button>
          ))}
        </div>
        <p className="description" style={{ marginTop: '20px' }}>What mood or feeling do you want your content to convey?</p>
        <div className="options">
          {['intimate', 'energetic', 'calm', 'mysterious'].map((opt) => (
            <button
              key={opt}
              onClick={() => {
                const newAnswer = { ...followupAnswer, mood: opt }
                setFollowupAnswer(newAnswer)
                onAnswer(newAnswer)
              }}
              className={`option ${followupAnswer.mood === opt ? 'selected' : ''}`}
            >
              {opt === 'intimate' ? 'Intimate/personal (close, authentic, vulnerable)' :
               opt === 'energetic' ? 'Energetic/upbeat (vibrant, dynamic, fun)' :
               opt === 'calm' ? 'Calm/peaceful (serene, contemplative, relaxed)' :
               'Mysterious/moody (atmospheric, dramatic, intriguing)'}
            </button>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="question">
      <h2>Visual Style</h2>
      <p className="description">What visual styles inspire your content? (Select all that apply)</p>
      <p className="note">Natural/outdoor and moody/atmospheric styles often perform well for indie artists. Consistent visual style helps with brand recognition.</p>
      <div className="options">
        {options.map((option) => (
          <button
            key={option.value}
            onClick={() => handleSelect(option.value)}
            className={`option ${Array.isArray(answer) && answer.includes(option.value) ? 'selected' : ''}`}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  )
}

// Upcoming music question with timeline follow-up
const UpcomingMusicQuestion = ({ answer, onAnswer }) => {
  const [showTimeline, setShowTimeline] = useState(false)
  const [musicType, setMusicType] = useState(null)

  const musicOptions = [
    { value: 'soon', label: "Yes, I have a single/EP/album coming out soon (I'll tell you when)" },
    { value: 'unreleased', label: 'Yes, I have unreleased music I want to build hype for' },
    { value: 'working', label: "I'm working on new music but don't have release dates yet" },
    { value: 'existing', label: 'I have existing music I want to promote' },
    { value: 'not_yet', label: "Not yet / I'm still creating" },
  ]

  const timelineOptions = [
    { value: 'within_month', label: 'Within the next month' },
    { value: '1_3_months', label: '1-3 months from now' },
    { value: '3_6_months', label: '3-6 months from now' },
    { value: '6_plus_months', label: '6+ months from now' },
    { value: 'flexible', label: "I'm not sure yet / flexible timeline" },
  ]

  const handleMusicSelect = (value) => {
    setMusicType(value)
    if (value === 'soon' || value === 'unreleased') {
      setShowTimeline(true)
    } else {
      onAnswer({ type: value })
    }
  }

  const handleTimelineSelect = (timeline) => {
    onAnswer({ type: musicType, timeline })
  }

  if (showTimeline) {
    return (
      <div className="question">
        <h2>Release Timeline</h2>
        <p className="description">Roughly when are you planning to release this music?</p>
        <p className="note">
          For releases within 1-3 months, I'll create a pre-release content strategy. For longer timelines, we'll focus on building your audience first, then ramp up promotion closer to release.
        </p>
        <div className="options">
          {timelineOptions.map((option) => (
            <button
              key={option.value}
              onClick={() => handleTimelineSelect(option.value)}
              className={`option ${answer?.timeline === option.value ? 'selected' : ''}`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="question">
      <h2>Upcoming Music</h2>
      <p className="description">Do you have any upcoming releases or music you want to promote in the next few months?</p>
      <p className="note">Planning content around releases can boost streams. If you have upcoming music, I'll help create a content calendar that builds anticipation and drives listeners to Spotify.</p>
      <div className="options">
        {musicOptions.map((option) => (
          <button
            key={option.value}
            onClick={() => handleMusicSelect(option.value)}
            className={`option ${answer?.type === option.value ? 'selected' : ''}`}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  )
}

// Upcoming content question (text input)
const UpcomingContentQuestion = ({ answer, onAnswer }) => {
  const [text, setText] = useState(answer || '')

  return (
    <div className="question">
      <h2>Upcoming Content</h2>
      <p className="description">
        Do you have any content you plan on posting soon? (e.g., "I have a music video coming out next week" or "I'm planning to post behind-the-scenes from my recording session")
      </p>
      <p className="note">This helps me prioritize and schedule your content more effectively.</p>
      <textarea
        value={text}
        onChange={(e) => {
          setText(e.target.value)
          onAnswer(e.target.value)
        }}
        placeholder="Tell me about any upcoming content you have planned..."
        className="text-input"
        rows={4}
        style={{ resize: 'vertical', minHeight: '100px' }}
      />
    </div>
  )
}

export default Onboarding

