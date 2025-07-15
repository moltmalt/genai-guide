"use client"

import { useEffect, useState } from "react"
import { CheckCircle, Package } from "lucide-react"

type OrderItem = {
  id?: number
  name: string
  size: string
  color: string
  price: string | number
  quantity: number
}

type CombinedOrderItem = {
  name: string
  totalQuantity: number
  totalPrice: number
  variants: { size: string; color: string; quantity: number; price: number }[]
}

function combineOrderItems(items: OrderItem[]): CombinedOrderItem[] {
  const map = new Map<string, CombinedOrderItem>()

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

    // Check if this variant already exists
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

function Order() {
  const [orders, setOrders] = useState<OrderItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchOrders = () => {
      fetch("http://127.0.0.1:8000/api/order")
        .then((res) => res.json())
        .then((data) => {
          setOrders(data)
          setLoading(false)
        })
        .catch((err) => {
          console.log("Failed to fetch orders: ", err)
          setLoading(false)
        })
    }
    fetchOrders()
    window.addEventListener("order-updated", fetchOrders)
    return () => window.removeEventListener("order-updated", fetchOrders)
  }, [])

  const combined = combineOrderItems(orders)
  const totalValue = combined.reduce((sum, item) => sum + item.totalPrice, 0)

  return (
    <div className="order-card">
      <div className="card-header">
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <CheckCircle size={16} color="#6366f1" />
          <h2 className="card-title">Orders</h2>
        </div>
        <p className="card-subtitle">
          {combined.length} orders • ${totalValue.toFixed(2)}
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
            <p>No orders yet</p>
          </div>
        ) : (
          <ul className="order-list">
            {combined.map((item) => (
              <li key={item.name} className="order-item">
                <div className="order-item-title">{item.name}</div>
                <div className="order-item-qty">
                  {item.totalQuantity} items • ${item.totalPrice.toFixed(2)}
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

export default Order
