import React, { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [query, setQuery] = useState('')
  const [typing, setTyping] = useState(false)
  const chatWindowRef = useRef()

  // Auto‑scroll on new messages
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTo({
        top: chatWindowRef.current.scrollHeight,
        behavior: 'smooth',
      })
    }
  }, [messages, typing])

  const sendMessage = async () => {
    if (!query.trim()) return

    // Your message
    const youMsg = {
      role: 'you',
      text: query,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }
    setMessages(prev => [...prev, youMsg])
    setQuery('')

    // Show typing indicator
    setTyping(true)
    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      const data = await res.json()
      const agentMsg = {
        role: 'agent',
        text: data.response,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
      setMessages(prev => [...prev, agentMsg])
    } catch (e) {
      setMessages(prev => [
        ...prev,
        {
          role: 'agent',
          text: 'Error contacting server',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ])
    } finally {
      setTyping(false)
    }
  }

  const handleKeyPress = e => {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="chat-container">
      <header className="chat-header">Google ADK Test 1</header>

      <div className="chat-window" ref={chatWindowRef} role="log" aria-live="polite">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="avatar">{msg.role === 'you' ? 'Y' : 'A'}</div>
            <div className="bubble-content">
              <div className="text">{msg.text}</div>
              <div className="timestamp">{msg.time}</div>
            </div>
          </div>
        ))}
        {typing && (
          <div className="typing-indicator">
            <div className="avatar">A</div>
            <div className="bubble-content">
              <div className="text">Agent is typing...</div>
            </div>
          </div>
        )}
      </div>

      <div className="input-row">
        <input
          type="text"
          placeholder="Type your message..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          aria-label="Message"
        />
        <button onClick={sendMessage} disabled={!query.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}

export default App
