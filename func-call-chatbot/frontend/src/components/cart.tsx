"use client"
import "../styles/index.css"

import { ShoppingCart, Package, CreditCard } from "lucide-react"
import { apiCall } from "../utils/api"

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

type CombinedCartItem = {
  name: string
  totalQuantity: number
  totalPrice: number
  image_url?: string
  variants: { size: string; color: string; quantity: number; price: number }[]
}

type CartGroup = {
  cart_id: string
  items: CombinedCartItem[]
  totalValue: number
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
        image_url: item.image_url,
        variants: [],
      })
    }

    const entry = map.get(item.name)!
    entry.totalQuantity += item.quantity
    entry.totalPrice += price * item.quantity // Calculate total price for this item

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

function groupCartsByCartId(items: CartItem[]): CartGroup[] {
  const cartGroups = new Map<string, CartGroup>()

  for (const item of items) {
    const cartId = item.cart_id
    const price = typeof item.price === "string" ? Number.parseFloat(item.price) : item.price
    
    if (!cartGroups.has(cartId)) {
      cartGroups.set(cartId, {
        cart_id: cartId,
        items: [],
        totalValue: 0
      })
    }
    
    const group = cartGroups.get(cartId)!
    const combinedItems = combineCartItems([item])
    
    // Merge with existing items in this cart
    const existingItem = group.items.find(i => i.name === combinedItems[0].name)
    if (existingItem) {
      existingItem.totalQuantity += combinedItems[0].totalQuantity
      existingItem.totalPrice += combinedItems[0].totalPrice
      // Merge variants
      combinedItems[0].variants.forEach(newVariant => {
        const existingVariant = existingItem.variants.find(v => 
          v.size === newVariant.size && v.color === newVariant.color
        )
        if (existingVariant) {
          existingVariant.quantity += newVariant.quantity
        } else {
          existingItem.variants.push(newVariant)
        }
      })
    } else {
      group.items.push(combinedItems[0])
    }
    
    // Recalculate total value for this cart group
    group.totalValue = group.items.reduce((sum, item) => sum + item.totalPrice, 0)
  }

  return Array.from(cartGroups.values())
}

interface CartProps {
  cart: CartItem[]
  setCart: (cart: CartItem[]) => void
  loading: boolean
  setLoading: (loading: boolean) => void
  onDataUpdate: (type: string) => void
}

function Cart({ cart, setCart, loading, setLoading, onDataUpdate }: CartProps) {

  // Cart component no longer makes API calls - only displays data from props
  // All cart data management is handled by App.tsx

  // Check if cart items have cart_id, if not, fall back to original display
  const hasCartId = cart.length > 0 && cart[0].hasOwnProperty('cart_id')
  
  let cartGroups: CartGroup[] = []
  let totalValue = 0
  
  if (hasCartId) {
    cartGroups = groupCartsByCartId(cart)
    totalValue = cartGroups.reduce((sum, group) => sum + group.totalValue, 0)
    console.log('Cart groups:', cartGroups)
  } else {
    // Fallback to original display
    const combined = combineCartItems(cart)
    totalValue = combined.reduce((sum, item) => sum + item.totalPrice, 0)
    console.log('Using fallback display, cart items:', cart)
  }

  return (
    <div className="cart-card">
      <div className="card-header">
        <div className="header-content">
          <ShoppingCart size={20} color="#6366f1" />
          <h2 className="card-title">Shopping Cart</h2>
        </div>
        <div className="header-stats">
          <span>{hasCartId ? `${cartGroups.length} ${cartGroups.length === 1 ? 'cart' : 'carts'}` : `${cart.length} ${cart.length === 1 ? 'item' : 'items'}`}</span>
          <span>•</span>
          <span>${totalValue.toFixed(2)} total</span>
        </div>
      </div>
      <div className="card-content">
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <div className="loading-text">Loading your cart...</div>
          </div>
        ) : (hasCartId ? cartGroups.length === 0 : cart.length === 0) ? (
          <div className="empty-state">
            <div className="empty-icon">
              <Package size={36} color="#94a3b8" />
            </div>
            <h3>Your cart is empty</h3>
            <p>Add some awesome t-shirts to get started!</p>
          </div>
        ) : hasCartId ? (
          <div className="cart-groups">
            {cartGroups.map((group) => (
              <div key={group.cart_id} className="cart-group">
                <div className="cart-group-header">
                  <div className="cart-group-info">
                    <h4>Cart #{group.cart_id.slice(0, 8)}</h4>
                    <span className="cart-group-item-count">{group.items.length} {group.items.length === 1 ? 'item' : 'items'}</span>
                  </div>
                  <div className="cart-group-summary">
                    <span className="cart-group-total">${group.totalValue.toFixed(2)}</span>
                    <button 
                      className="place-order-btn primary"
                      onClick={() => {
                        // Disable button to prevent double-clicking
                        const button = event?.target as HTMLButtonElement;
                        if (button) {
                          button.disabled = true;
                          button.textContent = 'Placing...';
                        }
                        
                        apiCall("http://127.0.0.1:8000/api/order/place", {
                          method: "POST"
                        })
                          .then((data: any) => {
                            // Show success message
                            alert('Order placed successfully!');
                            // Refresh cart data after order is placed
                            onDataUpdate('cart');
                            // Also refresh orders
                            onDataUpdate('orders');
                          })
                          .catch((err: any) => {
                            alert('Failed to place order. Please try again.');
                          })
                          .finally(() => {
                            // Re-enable button
                            if (button) {
                              button.disabled = false;
                              button.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>Place Order';
                            }
                          });
                      }}
                    >
                      <CreditCard size={14} />
                      Place Order
                    </button>
                  </div>
                </div>
                <div className="cart-items-container">
                  {group.items.map((item) => {
                    const convertedUrl = item.image_url ? item.image_url.replace('/object/sign/', '/object/public/').split('?')[0] : null;
                    
                    return (
                      <div key={item.name} className="cart-item">
                        <div className="cart-item-image-container">
                          <img 
                            src={convertedUrl || 'https://picsum.photos/300/200'} 
                            alt={item.name} 
                            className="cart-item-image" 
                            onError={(e) => {
                              e.currentTarget.src = 'https://picsum.photos/300/200';
                            }}
                          />
                        </div>
                        <div className="cart-item-info">
                          <h3 className="cart-item-title">{item.name}</h3>
                          <div className="cart-item-price">${item.totalPrice.toFixed(2)}</div>
                          <div className="cart-item-details">
                            <span className="quantity-badge">{item.totalQuantity} items</span>
                            {item.variants.map((variant: any, idx: number) => (
                              <span key={idx} className="variant-tag">
                                {variant.size} {variant.color} × {variant.quantity}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="cart-items-container">
            {combineCartItems(cart).map((item) => {
              const convertedUrl = item.image_url ? item.image_url.replace('/object/sign/', '/object/public/').split('?')[0] : null;
              
              return (
                <div key={item.name} className="cart-item">
                  <div className="cart-item-image-container">
                    <img 
                      src={convertedUrl || 'https://picsum.photos/300/200'} 
                      alt={item.name} 
                      className="cart-item-image" 
                      onError={(e) => {
                        e.currentTarget.src = 'https://picsum.photos/300/200';
                      }}
                    />
                  </div>
                  <div className="cart-item-info">
                    <h3 className="cart-item-title">{item.name}</h3>
                    <div className="cart-item-price">${item.totalPrice.toFixed(2)}</div>
                    <div className="cart-item-details">
                      <span className="quantity-badge">{item.totalQuantity} items</span>
                      {item.variants.map((variant: any, idx: number) => (
                        <span key={idx} className="variant-tag">
                          {variant.size} {variant.color} × {variant.quantity}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
            <div className="cart-summary">
              <div className="cart-total">
                <span className="total-label">Total:</span>
                <span className="total-amount">${totalValue.toFixed(2)}</span>
              </div>
            </div>
            <div className="cart-actions">
              <button 
                className="place-order-btn primary"
                onClick={() => {
                  // Disable button to prevent double-clicking
                  const button = event?.target as HTMLButtonElement;
                  if (button) {
                    button.disabled = true;
                    button.textContent = 'Placing...';
                  }
                  
                  apiCall("http://127.0.0.1:8000/api/order/place", {
                    method: "POST"
                  })
                    .then((data: any) => {
                      // Show success message
                      alert('Order placed successfully!');
                      // Refresh cart data after order is placed
                      onDataUpdate('cart');
                      // Also refresh orders
                      onDataUpdate('orders');
                    })
                    .catch((err: any) => {
                      alert('Failed to place order. Please try again.');
                    })
                    .finally(() => {
                      // Re-enable button
                      if (button) {
                        button.disabled = false;
                        button.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>Place Order';
                      }
                    });
                }}
              >
                <CreditCard size={14} />
                Place Order
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Cart
