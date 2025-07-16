"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { MessageCircle, Send } from "lucide-react"

interface Message {
  sender: "user" | "bot"
  text: string
}

function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    { sender: "bot", text: "Hello! How can I help you with t-shirts today?" },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = { sender: "user" as const, text: input }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.text }),
      })
      const data = await res.json()
      setMessages((prev) => [...prev, { sender: "bot", text: data.response || "Sorry, I didn't get that." }])

      // Trigger refresh if cart or order was updated
      if (data.response && /cart|added to cart/i.test(data.response)) {
        window.dispatchEvent(new Event("cart-updated"))
      }
      if (data.response && /order|placed|success/i.test(data.response)) {
        window.dispatchEvent(new Event("order-updated"))
      }
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Error communicating with server." }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-card">
      <div className="card-header">
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <MessageCircle size={20} color="#6366f1" />
          <h2 className="card-title">Chat Assistant</h2>
        </div>
        <p className="card-subtitle">Ask me anything about our t-shirts</p>
      </div>

      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`chat-message-row ${msg.sender === "user" ? "user" : "bot"}`}>
              <div className={`chat-bubble ${msg.sender}`}>{msg.text}</div>
            </div>
          ))}
          {loading && (
            <div className="chat-message-row bot">
              <div className="chat-bubble bot">
                <div className="loading-spinner"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="chat-input-area">
          <form className="chat-form" onSubmit={sendMessage}>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="chat-input"
              disabled={loading}
              rows={1}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  sendMessage(e)
                }
              }}
            />
            <button type="submit" className="chat-send-btn" disabled={loading || !input.trim()}>
              {loading ? <div className="loading-spinner"></div> : <Send size={16} />}
            </button>
          </form>
        </div>
    </div>
  )
}

export default Chat
