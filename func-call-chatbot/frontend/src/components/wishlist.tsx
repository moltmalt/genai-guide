"use client"
import "../products.css"

import { useEffect, useState } from "react"
import { Heart, Trash2 } from "lucide-react"
import { apiCall } from "../utils/api"

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

interface WishlistProps {
  wishlist: WishlistItem[]
  setWishlist: (wishlist: WishlistItem[]) => void
  loading: boolean
  setLoading: (loading: boolean) => void
  onDataUpdate: (type: string) => void
}

function Wishlist({ wishlist, setWishlist, loading, setLoading, onDataUpdate }: WishlistProps) {

  useEffect(() => {
    // Only fetch if we don't have wishlist data
    if (wishlist.length === 0 && loading) {
      apiCall("http://127.0.0.1:8000/api/wishlist", {
        method: "GET",
      })
        .then((data: any) => {
          setWishlist(data)
          setLoading(false)
        })
        .catch((err: any) => {
          setLoading(false)
        })
    }
    
    // Listen for wishlist-updated events
    window.addEventListener("wishlist-updated", () => {
      setLoading(true);
      apiCall("http://127.0.0.1:8000/api/wishlist", {
        method: "GET",
      })
        .then((data: any) => {
          setWishlist(data)
          setLoading(false)
        })
        .catch((err: any) => {
          setLoading(false)
        })
    });
    
    return () => window.removeEventListener("wishlist-updated", () => {});
  }, [wishlist.length, loading, setWishlist, setLoading])

  const removeFromWishlist = (variantId: string) => {
    apiCall("http://127.0.0.1:8000/api/wishlist/remove", {
      method: "DELETE",
      body: JSON.stringify({
        variant_id: variantId
      })
    })
      .then((data: any) => {
        // Refresh wishlist data
        setLoading(true);
        apiCall("http://127.0.0.1:8000/api/wishlist", {
          method: "GET",
        })
          .then((data: any) => {
            setWishlist(data)
            setLoading(false)
          })
          .catch((err: any) => {
            setLoading(false)
          })
      })
      .catch((err: any) => {
        // Handle error silently
      });
  }

  return (
    <div className="products-card">
      <div className="card-header">
        <div className="header-content">
          <Heart size={20} color="#6366f1" />
          <h2 className="card-title">Wishlist</h2>
        </div>
        <div className="header-stats">
          <span>{wishlist.length} {wishlist.length === 1 ? 'item' : 'items'}</span>
        </div>
      </div>
      <div className="card-content">
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <div className="loading-text">Loading wishlist...</div>
          </div>
        ) : wishlist.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <Heart size={36} color="#94a3b8" />
            </div>
            <div className="empty-title">Your wishlist is empty</div>
            <div className="empty-subtitle">Add some products to your wishlist to see them here</div>
          </div>
        ) : (
          <ul className="products-grid">
            {wishlist.map((item) => {
              const convertedUrl = item.image_url ? item.image_url.replace('/object/sign/', '/object/public/').split('?')[0] : null;
              
              return (
                <li key={item.id} className="product-card">
                  <div className="product-image-container">
                    <img 
                      src={convertedUrl || 'https://picsum.photos/300/200'} 
                      alt={item.name} 
                      className="product-image" 
                      onError={(e) => {
                        e.currentTarget.src = 'https://picsum.photos/300/200';
                      }}
                    />
                    <div className="stock-badge in">
                      In Stock
                    </div>
                  </div>
                  
                  <div className="product-info">
                    <h3 className="product-title">{item.name}</h3>
                    <div className="product-price">${item.price}</div>
                    
                    <div className="variants-section">
                      <div className="variants-title">Product Details</div>
                      <div className="variants-grid">
                        <div className="variant-card">
                          <div className="variant-size">Size {item.size}</div>
                          <div className="variant-price">${item.price}</div>
                          <div className="variant-stock">{item.stock} left</div>
                          <div className="variant-colors">
                            {item.color}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="product-actions">
                      <button 
                        className="action-btn secondary-btn"
                        onClick={() => removeFromWishlist(item.variant_id)}
                        style={{ backgroundColor: '#ef4444', color: 'white' }}
                      >
                        <Trash2 size={14} />
                        Remove
                      </button>
                    </div>
                  </div>
                </li>
              )
            })}
          </ul>
        )}
      </div>
    </div>
  )
}

export default Wishlist 