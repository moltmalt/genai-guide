import Product from "./components/products"
import Cart from "./components/cart"
import Order from "./components/order"
import Wishlist from "./components/wishlist"
import Login from "./components/login"
import Sidebar from "./components/sidebar"
import FloatingChat from "./components/floatingChat"
import { useState, useEffect } from "react"

// Type definitions
type ProductType = {
  variant_id: string
  name: string
  color: string
  price: number
  stock: number
  size: string
  image_url: string
}

type CartItem = {
  id?: number
  cart_id: string
  name: string
  size: string
  color: string
  price: string | number
  quantity: number
  image_url?: string
}

type OrderType = {
  order_id: string
  cart_id: string
  order_date: string
  status: string
  total_amount: number
  items: any[]
}

type WishlistItem = {
  id: string
  created_at: string
  variant_id: string
  name: string
  size: string
  color: string
  price: number
  stock: number
  image_url?: string
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [activeSection, setActiveSection] = useState("products")
  
  // Shared state for data
  const [products, setProducts] = useState<ProductType[]>([])
  const [cart, setCart] = useState<CartItem[]>([])
  const [wishlist, setWishlist] = useState<WishlistItem[]>([])
  const [orders, setOrders] = useState<OrderType[]>([])
  const [loading, setLoading] = useState({
    products: true,
    cart: true,
    wishlist: true,
    orders: true
  })

  useEffect(() => {
    const userId = localStorage.getItem("user_id")
    if (userId) {
      setIsLoggedIn(true)
      
      const fetchInitialData = async () => {
        try {
          const cartResponse = await fetch("http://127.0.0.1:8000/api/cart", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            }
          })
          if (cartResponse.ok) {
            const cartData = await cartResponse.json()
            setCart(cartData)
          }
          setLoading(prev => ({ ...prev, cart: false }))
          
          const productsResponse = await fetch("http://127.0.0.1:8000/api/tshirts", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            }
          })
          if (productsResponse.ok) {
            const productsData = await productsResponse.json()
            setProducts(productsData)
          }
          setLoading(prev => ({ ...prev, products: false }))
          
          const wishlistResponse = await fetch("http://127.0.0.1:8000/api/wishlist", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            }
          })
          if (wishlistResponse.ok) {
            const wishlistData = await wishlistResponse.json()
            setWishlist(wishlistData)
          }
          setLoading(prev => ({ ...prev, wishlist: false }))
          
          const ordersResponse = await fetch("http://127.0.0.1:8000/api/order/user", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            }
          })
          if (ordersResponse.ok) {
            const ordersData = await ordersResponse.json()
            setOrders(ordersData)
          }
          setLoading(prev => ({ ...prev, orders: false }))
          
        } catch (error) {
          console.error("Error fetching initial data:", error)
          setLoading({
            products: false,
            cart: false,
            wishlist: false,
            orders: false
          })
        }
      }
      
      fetchInitialData()
    }
  }, [])

  // Listen for cart-updated events from chatbot
  useEffect(() => {
    const handleCartUpdate = () => {
      console.log("Cart update event received from chatbot")
      refreshData('cart')
    }

    window.addEventListener('cart-updated', handleCartUpdate)
    return () => window.removeEventListener('cart-updated', handleCartUpdate)
  }, [])

  const handleLogout = () => {
    setIsLoggedIn(false)
    setActiveSection("products")
    setProducts([])
    setCart([])
    setWishlist([])
    setOrders([])
  }

  const [cartRefreshTimeout, setCartRefreshTimeout] = useState<NodeJS.Timeout | null>(null);

  const refreshData = (type: string) => {
    if (type === 'cart') {
      if (cartRefreshTimeout) {
        clearTimeout(cartRefreshTimeout);
      }
      
      // Set a new timeout to debounce cart refreshes
      const timeout = setTimeout(() => {
        console.log("Refreshing cart data...")
        // Set loading state for cart
        setLoading(prev => ({ ...prev, cart: true }))
        // Fetch updated cart data
        fetch("http://127.0.0.1:8000/api/cart", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`
          }
        })
          .then(res => res.json())
          .then(data => {
            console.log("Cart data received:", data)
            setCart(data)
            setLoading(prev => ({ ...prev, cart: false }))
          })
          .catch(err => {
            console.error("Failed to refresh cart:", err)
            setLoading(prev => ({ ...prev, cart: false }))
          })
      }, 1000); 
      
      setCartRefreshTimeout(timeout);
    } else if (type === 'wishlist') {
      window.dispatchEvent(new Event('wishlist-updated'))
    } else if (type === 'orders') {
      window.dispatchEvent(new Event('order-updated'))
    }
  }

  return isLoggedIn ? (
    <div className="app-container">
      <Sidebar 
        activeSection={activeSection}
        onSectionChange={setActiveSection}
        onLogout={handleLogout}
      />
      <div className="main-content">
        {activeSection === "products" && (
          <Product 
            products={products} 
            setProducts={setProducts}
            loading={loading.products}
            setLoading={(loading) => setLoading(prev => ({ ...prev, products: loading }))}
            onDataUpdate={refreshData}
          />
        )}
        {activeSection === "cart" && (
          <Cart 
            cart={cart} 
            setCart={setCart}
            loading={loading.cart}
            setLoading={(loading) => setLoading(prev => ({ ...prev, cart: loading }))}
            onDataUpdate={refreshData}
          />
        )}
        {activeSection === "wishlist" && (
          <Wishlist 
            wishlist={wishlist} 
            setWishlist={setWishlist}
            loading={loading.wishlist}
            setLoading={(loading) => setLoading(prev => ({ ...prev, wishlist: loading }))}
            onDataUpdate={refreshData}
          />
        )}
        {activeSection === "orders" && (
          <Order 
            orders={orders} 
            setOrders={setOrders}
            loading={loading.orders}
            setLoading={(loading) => setLoading(prev => ({ ...prev, orders: loading }))}
            onDataUpdate={refreshData}
          />
        )}
      </div>
      <FloatingChat />
    </div>
  ) : (
    <Login onLogin={() => setIsLoggedIn(true)} />
  )
}

export default App