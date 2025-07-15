import json
import os

BASE_DIR = "../mock-db/"
CART_DIR = os.path.join(BASE_DIR, "cart.json")
ORDER_DIR = os.path.join(BASE_DIR, "order.json")

def read_file(file_name):
    try:
        file_path = os.path.join(BASE_DIR, file_name)
        with open(file_path, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(f"Error: {e}")

def get_latest_id(file_name):
    data = read_file(file_name)
    if len(data) == 0:
        return 1
    latest_id = max(item["id"] for item in data)
    return latest_id + 1

def get_t_shirt(name, size, color):
    shirts = read_file("shirt.json")
    for shirt in shirts:
        if shirt["name"] == name and shirt["size"] == size and shirt["color"] == color:
            return shirt    
    return "No shirts found"

def add_to_cart(*, name, size, color, price, quantity):
    print(f"add_to_cart called with: name={name}, size={size}, color={color}, price={price}, quantity={quantity}")
    new_cart_item = {
        "id": get_latest_id("cart.json"),
        "name": name,
        "size": size,
        "color": color,
        "price": price,
        "quantity": quantity
    }

    cart = read_file("cart.json")
    cart.append(new_cart_item)

    with open(CART_DIR, "w") as f:
         json.dump(cart, f, indent=2)
    
    return cart

def place_order(*, name, size, color, price, quantity):
    print(f"place_order called with: name={name}, size={size}, color={color}, price={price}, quantity={quantity}")
    new_order = {
         "id": get_latest_id(ORDER_DIR),
         "name": name,
         "size": size,
         "color": color,
         "price": price,
         "quantity": quantity
    }

    order = read_file("order.json")
    order.append(new_order)

    with open(ORDER_DIR, "w") as f:
         json.dump(order, f, indent=2)

    return order