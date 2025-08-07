"use client"

import "../styles/index.css"
import type React from "react"

import { useState, useRef, useEffect } from "react"
import { MessageCircle, Send } from "lucide-react"
import { apiCall } from "../utils/api"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface ActionButton {
  label: string
  value: string
}

interface Message {
  sender: "user" | "bot"
  text: string
  actionButtons?: ActionButton[]
}

interface ChatProps {
  hideHeader?: boolean
}

function Chat({ hideHeader }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    { 
      sender: "bot", 
      text: "Hello! How can I help you with t-shirts today?",
      actionButtons: [
        { label: "Show Products", value: "show products" },
        { label: "View Cart", value: "view cart" },
        { label: "My Orders", value: "my orders" }
      ]
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleActionButtonClick = async (buttonValue: string) => {
    const userMessage = { sender: "user" as const, text: buttonValue }
    setMessages((prev) => [...prev, userMessage])
    setLoading(true)

    try {
      const data = await apiCall("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage.text }),
      })
      const botResponse = data.response || "Sorry, I didn't get that."
      
      // Check for cart refresh signal
      if (botResponse.includes("[REFRESH_CART]")) {
        // Remove the signal from the displayed message
        const cleanResponse = botResponse.replace("\n\n[REFRESH_CART]", "")
        setMessages((prev) => [...prev, { 
          sender: "bot", 
          text: cleanResponse,
          actionButtons: data.action_buttons || undefined
        }])
        
        // Trigger cart refresh
        window.dispatchEvent(new Event("cart-updated"))
      } else {
        setMessages((prev) => [...prev, { 
          sender: "bot", 
          text: botResponse,
          actionButtons: data.action_buttons || undefined
        }])
      }
      
      // Also check for order updates
      if (data.response && /order|placed|success/i.test(data.response)) {
        window.dispatchEvent(new Event("order-updated"))
      }
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Error communicating with server." }])
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = { sender: "user" as const, text: input }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const data = await apiCall("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage.text }),
      })
      const botResponse = data.response || "Sorry, I didn't get that."
      
      // Check for cart refresh signal
      if (botResponse.includes("[REFRESH_CART]")) {
        // Remove the signal from the displayed message
        const cleanResponse = botResponse.replace("\n\n[REFRESH_CART]", "")
        setMessages((prev) => [...prev, { 
          sender: "bot", 
          text: cleanResponse,
          actionButtons: data.action_buttons || undefined
        }])
        
        // Trigger cart refresh
        window.dispatchEvent(new Event("cart-updated"))
      } else {
        setMessages((prev) => [...prev, { 
          sender: "bot", 
          text: botResponse,
          actionButtons: data.action_buttons || undefined
        }])
      }
      
      // Also check for order updates
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
      {!hideHeader && (
        <div className="card-header">
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <MessageCircle size={20} color="#6366f1" />
            <h2 className="card-title">Chat Assistant</h2>
          </div>
          <p className="card-subtitle">Ask me anything about our t-shirts</p>
        </div>
      )}

      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`chat-message-row ${msg.sender === "user" ? "user" : "bot"}`}>
              <div className={`chat-bubble ${msg.sender}`}>
                {msg.sender === "bot" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
                ) : (
                  msg.text
                )}
                {msg.sender === "bot" && msg.actionButtons && (
                  <div className="action-buttons">
                    {msg.actionButtons.map((button, buttonIdx) => (
                      <button
                        key={buttonIdx}
                        className="action-button"
                        onClick={() => handleActionButtonClick(button.value)}
                        disabled={loading}
                      >
                        {button.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>
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
