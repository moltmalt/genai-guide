import "./index.css"
import Product from "./components/products"
import Chat from "./components/chat"
import Cart from "./components/cart"
import Order from "./components/order"

function App() {
  return (
    <div className="main-grid">
      <div className="products-section">
        <Product />
      </div>
      <div className="chat-section">
        <Chat />
      </div>
      <div className="right-section">
        <Cart />
        <Order />
      </div>
    </div>
  )
}

export default App
