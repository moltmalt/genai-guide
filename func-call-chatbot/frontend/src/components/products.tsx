"use client"

import { useEffect, useState } from "react"
import { Package, Shirt } from "lucide-react"

type ProductType = {
  id: number
  name: string
  color: string
  price: number
  quantity: number
  size: string
}

type CombinedProduct = {
  name: string
  totalQuantity: number
  variants: { [key: string]: { colors: string[]; price: number; quantity: number } }
}

function combineProducts(items: ProductType[]): CombinedProduct[] {
  const map = new Map<string, CombinedProduct>()

  for (const item of items) {
    if (!map.has(item.name)) {
      map.set(item.name, {
        name: item.name,
        totalQuantity: 0,
        variants: {},
      })
    }

    const entry = map.get(item.name)!
    entry.totalQuantity += item.quantity

    const sizeKey = item.size
    if (!entry.variants[sizeKey]) {
      entry.variants[sizeKey] = {
        colors: [],
        price: item.price,
        quantity: 0,
      }
    }

    if (!entry.variants[sizeKey].colors.includes(item.color)) {
      entry.variants[sizeKey].colors.push(item.color)
    }
    entry.variants[sizeKey].quantity += item.quantity
  }

  return Array.from(map.values())
}

function getProductImage(productName: string): string {
  const imageMap: { [key: string]: string } = {
    "My AI is Smarter Than Your Honor Student": "/images/my-ai-is-smarter.png",
    "Keep Calm and Trust the Neural Network": "/images/keep-calm.png",
    "I’m Just Here for the Deep Learning": "/images/im-just-here-dl.png",
  }
  return imageMap[productName] || "/images/default.svg";
}

function Product() {
  const [products, setProducts] = useState<ProductType[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/tshirts")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data)
        setLoading(false)
      })
      .catch((err) => {
        console.log("Failed to fetch products: ", err)
        setLoading(false)
      })
  }, [])

  const combined = combineProducts(products)

  return (
    <div className="products-card">
      <div className="card-header">
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <Package size={18} color="#6366f1" />
          <h2 className="card-title">Products</h2>
        </div>
        <p className="card-subtitle">
          {combined.length} designs • {products.reduce((sum, p) => sum + p.quantity, 0)} total items
        </p>
      </div>
      <div className="card-content">
        {loading ? (
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "150px" }}>
            <div className="loading-spinner"></div>
          </div>
        ) : combined.length === 0 ? (
          <div className="empty-msg">
            <Shirt size={28} color="#94a3b8" style={{ marginBottom: "8px" }} />
            <p>No products available</p>
          </div>
        ) : (
          <ul className="products-list">
            {combined.map((item) => (
              <li key={item.name} className="products-item">
                <img src={getProductImage(item.name) || "/placeholder.svg"} alt={item.name} className="product-image" />
                <div className="product-info">
                  <div className="products-item-title">{item.name}</div>
                  <div className="products-item-qty">{item.totalQuantity} in stock</div>
                  <div className="variant-grid">
                    {Object.entries(item.variants).map(([size, variant]) => (
                      <div key={size} className="variant-item">
                        <div className="variant-size">Size {size}</div>
                        <div className="variant-details">
                          ${variant.price} • {variant.quantity} left
                        </div>
                        <div className="variant-details">{variant.colors.join(", ")}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default Product
