import json

def read_file(file_name):
    try:
        with open(f"mock-db/{file_name}") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(f"Error: {e}")

def get_t_shirt(name, size, color):
    shirts = read_file("shirt.json")
    for shirt in shirts:
                if shirt["name"] == name and shirt["size"] == size and shirt["color"] == color:
                    return shirt
                
    return "No shirts found"

def add_to_cart(name, size, color, price, quantity):
    new_cart_item = {
         "name": name,
         "size": size,
         "color": color,
         "price": price,
         "quantity": quantity
    }

    cart = read_file("cart.json")
    cart.append(new_cart_item)

    with open("mock-db/cart.json", "w") as f:
         json.dump(cart, f, indent=2)
    
    return cart

def place_order(name, size, color, price, quantity):
    new_order = {
         "name": name,
         "size": size,
         "color": color,
         "price": price,
         "quantity": quantity
    }

    order = read_file("order.json")
    order.append(new_order)

    with open("mock-db/order.json", "w") as f:
         json.dump(order, f, indent=2)

    return order