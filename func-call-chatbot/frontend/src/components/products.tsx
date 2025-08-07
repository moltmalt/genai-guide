"use client"
import "../products.css"

import { useEffect, useState } from "react"
import { Package, Shirt, ShoppingCart, Heart } from "lucide-react"
import { apiCall } from "../utils/api"

type ProductType = {
  variant_id: string
  name: string
  color: string
  price: number
  stock: number
  size: string
  image_url: string
}

type CombinedProduct = {
  name: string
  totalQuantity: number
  image_url: string
  variants: { [key: string]: { colors: string[]; price: number; stock: number } }
}

function combineProducts(items: ProductType[]): CombinedProduct[] {
  const map = new Map<string, CombinedProduct>()

  for (const item of items) {
    if (!map.has(item.name)) {
      map.set(item.name, {
        name: item.name,
        totalQuantity: 0,
        image_url: item.image_url,
        variants: {},
      })
    }

    const entry = map.get(item.name)!
    entry.totalQuantity += item.stock

    const sizeKey = item.size
    if (!entry.variants[sizeKey]) {
      entry.variants[sizeKey] = {
        colors: [],
        price: item.price,
        stock: 0,
      }
    }

    if (!entry.variants[sizeKey].colors.includes(item.color)) {
      entry.variants[sizeKey].colors.push(item.color)
    }
    entry.variants[sizeKey].stock += item.stock
  }

  return Array.from(map.values())
}



interface ProductProps {
  products: ProductType[]
  setProducts: (products: ProductType[]) => void
  loading: boolean
  setLoading: (loading: boolean) => void
  onDataUpdate: (type: string) => void
}

function Product({ products, setProducts, loading, setLoading, onDataUpdate }: ProductProps) {

  useEffect(() => {
    // Only fetch if we don't have products data
    if (products.length === 0 && loading) {
      apiCall("http://127.0.0.1:8000/api/tshirts", {
        method: "GET",
      })
        .then((data: any) => {
          console.log("Products data:", data);
          setProducts(data)
          setLoading(false)
        })
        .catch((err: any) => {
          console.log("Failed to fetch products: ", err)
          setLoading(false)
        })
    }
  }, [products.length, loading, setProducts, setLoading])

  const combined = combineProducts(products)

  const getStockStatus = (quantity: number) => {
    if (quantity === 0) return { status: 'out', text: 'Out of Stock' }
    if (quantity < 5) return { status: 'low', text: 'Low Stock' }
    return { status: 'in', text: 'In Stock' }
  }

  const getLowestPrice = (variants: { [key: string]: { colors: string[]; price: number; stock: number } }) => {
    return Math.min(...Object.values(variants).map(v => v.price))
  }

  return (
    <div className="products-card">
      <div className="card-header">
        <div className="header-content">
          <Package size={20} color="#6366f1" />
          <h2 className="card-title">Products</h2>
        </div>
        <div className="header-stats">
          <span>{combined.length} designs</span>
          <span>•</span>
          <span>{products.reduce((sum, p) => sum + p.stock, 0)} total items</span>
        </div>
      </div>
      <div className="card-content">
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <div className="loading-text">Loading products...</div>
          </div>
        ) : combined.length === 0 ? (
          <div className="empty-state">
                      <div className="empty-icon">
            <Shirt size={36} />
          </div>
            <div className="empty-title">No products available</div>
            <div className="empty-subtitle">Check back later for new arrivals</div>
          </div>
        ) : (
          <ul className="products-grid">
            {combined.map((item) => {
              const stockStatus = getStockStatus(item.totalQuantity)
              const lowestPrice = getLowestPrice(item.variants)
              
              const convertedUrl = item.image_url ? item.image_url.replace('/object/sign/', '/object/public/').split('?')[0] : null;
              console.log('Product image URL:', item.name, item.image_url);
              console.log('Converted URL:', item.name, convertedUrl);
              
              return (
                <li key={item.name} className="product-card">
                  <div className="product-image-container">
                    <img 
                      src={convertedUrl || 'https://picsum.photos/300/200'} 
                      alt={item.name} 
                      className="product-image" 
                      onError={(e) => {
                        console.log('Image failed to load:', e.currentTarget.src);
                        // Use placeholder image as fallback
                        e.currentTarget.src = 'https://picsum.photos/300/200';
                      }}
                      onLoad={(e) => {
                        console.log('Image loaded successfully:', e.currentTarget.src);
                      }}
                    />
                    <div className={`stock-badge ${stockStatus.status}`}>
                      {stockStatus.text}
                    </div>
                  </div>
                  
                  <div className="product-info">
                    <h3 className="product-title">{item.name}</h3>
                    <div className="product-price">From ${lowestPrice}</div>
                    
                    <div className="variants-section">
                      <div className="variants-title">Available Sizes</div>
                      <div className="variants-grid">
                        {Object.entries(item.variants).map(([size, variant]) => (
                          <div key={size} className="variant-card">
                            <div className="variant-size">Size {size}</div>
                            <div className="variant-price">${variant.price}</div>
                            <div className="variant-stock">{variant.stock} left</div>
                            <div className="variant-colors">
                              {variant.colors.slice(0, 2).join(", ")}
                              {variant.colors.length > 2 && "..."}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="product-actions">
                      <button 
                        className="action-btn secondary-btn"
                        onClick={() => {
                          // For now, we'll add the first variant. You might want to add a size/color selector
                          const firstVariant = Object.entries(item.variants)[0];
                          if (firstVariant) {
                            const [size, variant] = firstVariant;
                            // Find the product with this size and first color
                            let product = products.find(p => p.name === item.name && p.size === size);
                            
                            // If not found, try to find any product with the same name
                            if (!product) {
                              product = products.find(p => p.name === item.name);
                            }
                            
                            // Use variant_id directly since that's the correct field name
                            const productId = product?.variant_id;
                            
                            if (product && productId) {
                              // Disable button to prevent double-clicking
                              const button = event?.target as HTMLButtonElement;
                              if (button) {
                                button.disabled = true;
                                button.textContent = 'Adding...';
                              }
                              
                              const requestBody = {
                                variant_id: productId.toString()
                              };
                              
                              apiCall("http://127.0.0.1:8000/api/wishlist/add", {
                                method: "POST",
                                body: JSON.stringify(requestBody)
                              })
                                .then((data: any) => {
                                  // Show success feedback
                                  if (button) {
                                    button.textContent = 'Added!';
                                    setTimeout(() => {
                                      button.disabled = false;
                                      button.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>Wishlist';
                                    }, 1000);
                                  }
                                  // Trigger wishlist update event
                                  window.dispatchEvent(new Event('wishlist-updated'));
                                })
                                .catch((err: any) => {
                                  // Re-enable button on error
                                  if (button) {
                                    button.disabled = false;
                                    button.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>Wishlist';
                                  }
                                });
                            }
                          }
                        }}
                      >
                        <Heart size={14} />
                        Wishlist
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

export default Product
