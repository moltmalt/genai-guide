"use client"

import { useEffect, useState } from "react"
import { ShoppingCart, Package } from "lucide-react"

type CartItem = {
  id?: number
  name: string
  size: string
  color: string
  price: string | number
  quantity: number
}

type CombinedCartItem = {
  name: string
  totalQuantity: number
  totalPrice: number
  variants: { size: string; color: string; quantity: number; price: number }[]
}

function combineCartItems(items: CartItem[]): CombinedCartItem[] {
  const map = new Map<string, CombinedCartItem>()

  for (const item of items) {
    const price = typeof item.price === "string" ? Number.parseFloat(item.price) : item.price

    if (!map.has(item.name)) {
      map.set(item.name, {
        name: item.name,
        totalQuantity: 0,
        totalPrice: 0,
        variants: [],
      })
    }

    const entry = map.get(item.name)!
    entry.totalQuantity += item.quantity
    entry.totalPrice = price

    const existingVariant = entry.variants.find((v) => v.size === item.size && v.color === item.color)
    if (existingVariant) {
      existingVariant.quantity += item.quantity
    } else {
      entry.variants.push({
        size: item.size,
        color: item.color,
        quantity: item.quantity,
        price: price,
      })
    }
  }

  return Array.from(map.values())
}

function Cart() {
  const [cart, setCart] = useState<CartItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchCart = () => {
      fetch("http://127.0.0.1:8000/api/cart")
        .then((res) => res.json())
        .then((data) => {
          setCart(data)
          setLoading(false)
        })
        .catch((err) => {
          console.log("Failed to fetch cart: ", err)
          setLoading(false)
        })
    }

    fetchCart();
    window.addEventListener("cart-updated", fetchCart);
    return () => window.removeEventListener("cart-updated", fetchCart);
  }, []);

  const combined = combineCartItems(cart)
  const totalValue = combined.reduce((sum, item) => sum + item.totalPrice, 0)

  return (
    <div className="cart-card">
      <div className="card-header">
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <ShoppingCart size={16} color="#6366f1" />
          <h2 className="card-title">Cart</h2>
        </div>
        <p className="card-subtitle">
          {combined.length} items • ${totalValue.toFixed(2)}
        </p>
      </div>
      <div className="card-content">
        {loading ? (
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "80px" }}>
            <div className="loading-spinner"></div>
          </div>
        ) : combined.length === 0 ? (
          <div className="empty-msg">
            <Package size={20} color="#94a3b8" style={{ marginBottom: "6px" }} />
            <p>Your cart is empty</p>
          </div>
        ) : (
          <ul className="cart-list">
            {combined.map((item) => (
              <li key={item.name} className="cart-item">
                <div className="cart-item-title">{item.name}</div>
                <div className="cart-item-qty">
                  {item.totalQuantity} items • ${item.totalPrice}
                </div>
                <div className="item-variants">
                  {item.variants.map((variant, idx) => (
                    <span key={idx} className="variant-tag">
                      {variant.size} {variant.color} × {variant.quantity}
                    </span>
                  ))}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default Cart
