import { useState, useEffect } from "react"
import { 
  Package, 
  ShoppingCart, 
  FileText, 
  LogOut, 
  User,
  Menu,
  X,
  Info,
  ChevronRight,
  HelpCircle,
  Heart,
  Cpu
} from "lucide-react"
import "../styles/sidebar.css"

interface SidebarProps {
  activeSection: string
  onSectionChange: (section: string) => void
  onLogout: () => void
}

export default function Sidebar({ activeSection, onSectionChange, onLogout }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [userEmail, setUserEmail] = useState("")
  const [userName, setUserName] = useState("")
  const [showLogoutPopup, setShowLogoutPopup] = useState(false)

  useEffect(() => {
    const email = localStorage.getItem("user_email")
    if (email) {
      setUserEmail(email)
      const name = email.split('@')[0]
      setUserName(name)
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem("user_id")
    localStorage.removeItem("user_email")
    setShowLogoutPopup(false)
    onLogout()
  }

  const toggleLogoutPopup = () => {
    setShowLogoutPopup(!showLogoutPopup)
  }

  const navItems = [
    { id: "products", label: "Products", icon: Package },
    { id: "wishlist", label: "Wishlist", icon: Heart },
    { id: "cart", label: "Cart", icon: ShoppingCart },
    { id: "orders", label: "Orders", icon: FileText },
  ]

  return (
    <>
      {/* mobile menu button */}
      <button
        className="mobile-menu-btn"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle menu"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* sidebar overlay for mobile */}
      {isOpen && (
        <div className="sidebar-overlay" onClick={() => setIsOpen(false)} />
      )}

      {/* Sidebar */}
      <div className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        {/* Top Branding Section */}
        <div className="sidebar-header">
          <div className="brand-section">
            <div className="brand-icon">
              <Cpu size={20} color="#ffffff" />
            </div>
            <div className="brand-name">ChatFit</div>
            <div className="brand-info">
              <Info size={14} />
            </div>
          </div>
        </div>

        {/* main Menu Section */}
        <nav className="sidebar-nav">
          <div className="menu-section">
            <div className="menu-title">Main Menu</div>
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <button
                  key={item.id}
                  className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
                  onClick={() => {
                    onSectionChange(item.id)
                    setIsOpen(false) // Close mobile menu
                  }}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </button>
              )
            })}
          </div>
        </nav>

        {/* Footer Section */}
        <div className="sidebar-footer">
          <div className="help-section">
            <button className="help-item">
              <HelpCircle size={18} />
              <span>Help Center</span>
            </button>
          </div>
          
          <div className="user-profile-section">
            <div className="user-profile-card" onClick={toggleLogoutPopup}>
              <div className="user-avatar">
                <User size={18} />
              </div>
              <div className="user-details">
                <div className="user-name">{userName}</div>
                <div className="user-email">{userEmail}</div>
              </div>
              <div className="profile-arrow">
                <ChevronRight size={16} />
              </div>
            </div>
            
            {/* Logout Popup */}
            <div className={`logout-popup ${showLogoutPopup ? 'show' : ''}`}>
              <button className="logout-btn" onClick={handleLogout}>
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
} 