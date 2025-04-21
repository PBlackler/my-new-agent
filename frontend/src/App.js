import React, { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([])  // [{ from: 'you'|'agent', text }]

  const sendMessage = async () => {
    if (!query.trim()) return
    setMessages(prev => [...prev, { from: 'you', text: query }])
    setQuery('')

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const { response, error } = await res.json()
      setMessages(prev => [
        ...prev,
        { from: 'agent', text: error || response }
      ])
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { from: 'agent', text: 'Error contacting server' }
      ])
    }
  }

  const handleKey = e => {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="chat-container">
      <h1>Chat with Agent</h1>
      <div className="chat-window">
        {messages.map((m, i) => (
          <div
            key={i}
            className={m.from === 'you' ? 'message you' : 'message agent'}
          >
            <strong>{m.from === 'you' ? 'You' : 'Agent'}:</strong>{' '}
            {m.text}
          </div>
        ))}
      </div>
      <div className="input-row">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Type a message…"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )
}

export default App
