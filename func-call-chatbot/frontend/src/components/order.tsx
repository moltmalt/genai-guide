"use client"
import "../styles/index.css"

import { useEffect, useState } from "react"
import { Package, ShoppingBag, Calendar, DollarSign, Trash2 } from "lucide-react"
import { apiCall } from "../utils/api"

type OrderItem = {
  id: string
  order_item_id: string
  name: string
  size: string
  color: string
  price: number
  quantity: number
  stock: number
}

type Order = {
  order_id: string
  cart_id: string
  order_date: string
  status: string
  total_amount: number
  items: OrderItem[]
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
    entry.totalPrice += item.price * item.quantity

    const existingVariant = entry.variants.find((v) => v.size === item.size && v.color === item.color)
    if (existingVariant) {
      existingVariant.quantity += item.quantity
    } else {
      entry.variants.push({
        size: item.size,
        color: item.color,
        quantity: item.quantity,
        price: item.price,
      })
    }
  }

  return Array.from(map.values())
}

function calculateOrderTotal(items: OrderItem[]): number {
  return items.reduce((total, item) => total + (item.price * item.quantity), 0)
}

interface OrderProps {
  orders: Order[]
  setOrders: (orders: Order[]) => void
  loading: boolean
  setLoading: (loading: boolean) => void
  onDataUpdate: (type: string) => void
}

function Order({ orders, setOrders, loading, setLoading, onDataUpdate }: OrderProps) {

  useEffect(() => {
    const fetchOrders = () => {
      apiCall("http://127.0.0.1:8000/api/order/user", {
        method: "GET",
      })
        .then((data) => {
          setOrders(data)
          setLoading(false)
        })
        .catch((err) => {
          console.log("Failed to fetch orders: ", err)
          setLoading(false)
        })
    }

    // Only fetch if we don't have orders data
    if (orders.length === 0 && loading) {
      fetchOrders()
    }
    
    window.addEventListener("order-updated", fetchOrders)
    return () => window.removeEventListener("order-updated", fetchOrders)
  }, [orders.length, loading, setOrders, setLoading])

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pending': return '#f59e0b'
      case 'processing': return '#3b82f6'
      case 'shipped': return '#8b5cf6'
      case 'delivered': return '#10b981'
      case 'cancelled': return '#ef4444'
      default: return '#6b7280'
    }
  }

  const deleteOrder = (orderId: string) => {
    apiCall(`http://127.0.0.1:8000/api/order/${orderId}`, {
      method: "DELETE"
    })
      .then((data: any) => {
        // Remove the order from the local state
        setOrders(orders.filter(order => order.order_id !== orderId));
      })
      .catch((err: any) => {
        // Handle error silently
      });
  }

  return (
    <div className="orders-card">
      <div className="card-header">
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <ShoppingBag size={16} color="#6366f1" />
          <h2 className="card-title">Orders</h2>
        </div>
        <p className="card-subtitle">
          {orders.length} orders • ${orders.reduce((sum, order) => sum + calculateOrderTotal(order.items), 0).toFixed(2)} total
        </p>
      </div>
      <div className="card-content">
        {loading ? (
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "80px" }}>
            <div className="loading-spinner"></div>
          </div>
        ) : orders.length === 0 ? (
          <div className="empty-msg">
            <Package size={20} color="#94a3b8" style={{ marginBottom: "6px" }} />
            <p>No orders yet</p>
          </div>
        ) : (
          <div className="orders-list">
            {orders.map((order) => {
              const combined = combineOrderItems(order.items)
              return (
                <div key={order.order_id} className="order-card">
                  <div className="order-header">
                    <div className="order-info">
                      <div className="order-id">Order #{order.order_id.slice(0, 8)}</div>
                      <div className="order-date">
                        <Calendar size={12} />
                        {formatDate(order.order_date)}
                      </div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <div className={`order-status ${order.status.toLowerCase()}`}>
                        {order.status}
                      </div>
                      <button
                        className="delete-order-btn"
                        onClick={() => deleteOrder(order.order_id)}
                        title="Delete order"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                  
                  <div className="order-items">
                    {combined.map((item) => (
                      <div key={item.name} className="order-item">
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
                      </div>
                    ))}
                  </div>
                  
                  <div className="order-total">
                    <span>Total: ${calculateOrderTotal(order.items).toFixed(2)}</span>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default Order
