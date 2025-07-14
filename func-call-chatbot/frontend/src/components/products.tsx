import { useEffect, useState } from "react";

type ProductType = { 
    id: number
    name: string
    color: string
    price: number
    quantity: number
}; 

function Product(){

    const [products, setProducts] = useState<ProductType[]>([]);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/products")
        .then((res) => res.json())
        .then((data) => setProducts(data))
        .catch((err) => console.log("Failed to fetch products: ", err))
    }, [])

    return(
        <div>
            <ul>
                {products.map((item) => (
                    <li key={item.id}>
                        <p>{item.name}</p>
                        <p>{item.color}</p>
                        <p>{item.price}</p>
                        <p>{item.quantity}</p>
                    </li>
                ))}
            </ul>
            
        </div>
    )
}

export default Product