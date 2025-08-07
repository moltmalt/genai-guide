import { useState } from "react"
import { Bot, X } from "lucide-react"
import Chat from "./chat"
import "../products.css" 

export default function FloatingChat() {
  const [open, setOpen] = useState(false)

  const handleToggle = () => setOpen((prev) => !prev)

  return (
    <>
      {/* Floating Button (always visible, toggles chat) */}
      <button
        className="floating-chat-btn purple"
        onClick={handleToggle}
        aria-label={open ? "Close chat" : "Open chat"}
        style={open ? { zIndex: 1302 } : {}}
      >
        <Bot size={28} />
      </button>

      {/* Chat Modal/Panel */}
      {open && (
        <div className="floating-chat-modal-bg">
          <div className="floating-chat-modal improved">
            <div className="floating-chat-header">
              <div className="floating-chat-header-left">
                <span className="floating-chat-header-icon"><Bot size={22} /></span>
                <span className="floating-chat-header-title">Chat Assistant</span>
              </div>
              <button
                className="floating-chat-close"
                onClick={handleToggle}
                aria-label="Close chat"
              >
                <X size={22} />
              </button>
            </div>
            <div className="floating-chat-content">
              <Chat hideHeader />
            </div>
          </div>
        </div>
      )}
    </>
  )
} 