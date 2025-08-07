"use client"

import type React from "react"
import "../styles/auth.css"

import { useState, useCallback } from "react"
import { Eye, EyeOff, Mail, Lock, AlertCircle, MessageCircle, Globe } from "lucide-react"

interface LoginProps {
  onLogin?: () => void
  loading?: boolean
}

export default function Login({ onLogin, loading: externalLoading }: LoginProps) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [fieldErrors, setFieldErrors] = useState<{ email?: string; password?: string }>({})

  const isLoading = loading || externalLoading

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const validateForm = useCallback(() => {
    const errors: { email?: string; password?: string } = {}

    if (!email.trim()) {
      errors.email = "Email is required"
    } else if (!validateEmail(email)) {
      errors.email = "Invalid email address"
    }

    if (!password) {
      errors.password = "Password is required"
    } else if (password.length < 8) {
      errors.password = "Password must be at least 8 characters"
    }

    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }, [email, password])

  const handleSubmit = async (e?: React.FormEvent | React.MouseEvent) => {
    e?.preventDefault()
    setError("")

    if (!validateForm()) {
      return
    }

    setLoading(true)
    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/sign_in", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify({ email: email.trim(), password: password }),
      })

      if (!response.ok) {
        if (response.status === 401 || response.status === 500) {
          throw new Error("Incorrect email/password")
        } else if (response.status === 422) {
          throw new Error("Invalid input data")
        } else if (response.status >= 500) {
          throw new Error("Server error. Please try again later.")
        } else {
          throw new Error(`Login failed (${response.status})`)
        }
      }

      const data = await response.json()
      console.log("JSON data", data)
      
      // Store user data
      localStorage.setItem("user_id", data["user_id"])
      localStorage.setItem("user_email", email.trim())

      if (data.data && data.data.access_token) {
        localStorage.setItem("access_token", data.data.access_token)
      }

      console.log("Access Token Log", localStorage.getItem("access_token"))
      
      // Call onLogin callback after successful login
      if(onLogin) onLogin()

    } catch (err: any) {
      setError(err.message || "Login failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-form-section">
        <div className="login-card">
          <div className="card-header">
            <h2 className="card-title">Welcome Back</h2>
            <p className="card-subtitle">Sign in to your account to continue</p>
          </div>

          <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email" className="form-label">
                <Mail size={16} />
                Email Address
              </label>
              <div className="input-wrapper">
                <input
                  id="email"
                  type="email"
                  className={`form-input ${fieldErrors.email ? "error" : ""} ${email ? "filled" : ""}`}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="email"
                  required
                  disabled={isLoading}
                  placeholder="Enter your email"
                />
                <div className="input-focus-border"></div>
              </div>
              {fieldErrors.email && (
                <div className="form-error">
                  <AlertCircle size={14} />
                  {fieldErrors.email}
                </div>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">
                <Lock size={16} />
                Password
              </label>
              <div className="input-wrapper password-wrapper">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  className={`form-input ${fieldErrors.password ? "error" : ""} ${password ? "filled" : ""}`}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                  disabled={isLoading}
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
                <div className="input-focus-border"></div>
              </div>
              {fieldErrors.password && (
                <div className="form-error">
                  <AlertCircle size={14} />
                  {fieldErrors.password}
                </div>
              )}
            </div>

            {error && (
              <div className="form-error global-error">
                <AlertCircle size={16} />
                {error}
              </div>
            )}

            <button type="submit" className="login-btn" disabled={isLoading}>
              <span className="btn-content">
                {isLoading ? (
                  <>
                    <div className="loading-spinner"></div>
                    Signing in...
                  </>
                ) : (
                  "Sign In"
                )}
              </span>
              <div className="btn-shine"></div>
            </button>
          </form>
        </div>
      </div>

      <div className="login-design-section">
        <div className="floating-elements">
          <div className="floating-element"></div>
          <div className="floating-element"></div>
          <div className="floating-element"></div>
          <div className="floating-element"></div>
          <div className="floating-element"></div>
        </div>

        <div className="design-content">
          <div className="design-title">
            <img src="/images/woman-chat.svg" alt="Customer Service Representative" style={{ height: '240px', width: 'auto' }} />
          </div>
          <p className="design-subtitle">
            Experience seamless customer support with our AI-powered chatbot. 
            Get instant help, 24/7 assistance, and personalized solutions.
          </p>
          
          <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', marginTop: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '14px' }}>
              <MessageCircle size={20} />
              <span>Live Chat</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '14px' }}>
              <Globe size={20} />
              <span>24/7 Support</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
