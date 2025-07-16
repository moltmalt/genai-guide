import json
import os

BASE_DIR = "func-call-chatbot/mock-db"
SHIRT_DIR = os.path.join(BASE_DIR, "shirt.json")
CART_DIR = os.path.join(BASE_DIR, "cart.json")
ORDER_DIR = os.path.join(BASE_DIR, "order.json")

def read_file(file_name):
    try:
        file_path = os.path.join(file_name)
        with open(file_path, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(f"Error: {e}")

def get_latest_id(file_name):
    print(file_name)
    data = read_file(file_name)
    if len(data) == 0:
        return 1
    latest_id = max(item["id"] for item in data)
    return latest_id + 1

def get_t_shirt(name, size, color):
    shirts = read_file(SHIRT_DIR)
    for shirt in shirts:
        if shirt["name"] == name and shirt["size"] == size and shirt["color"] == color:
            return shirt    
    return "No shirts found"

def add_to_cart(*, name, size, color, price, quantity):
    print(f"add_to_cart called with: name={name}, size={size}, color={color}, price={price}, quantity={quantity}")
    new_cart_item = {
        "id": get_latest_id(CART_DIR),
        "name": name,
        "size": size,
        "color": color,
        "price": price,
        "quantity": quantity
    }

    cart = read_file(CART_DIR)

    for item in cart:
        if item["name"] == new_cart_item["name"] and item["size"] == new_cart_item["size"] and item["color"] == new_cart_item["color"]:
            item["quantity"] = item["quantity"] + new_cart_item["quantity"]
            break
    else:
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

    order = read_file(ORDER_DIR)

    for item in order:
        if item["name"] == new_order["name"] and item["size"] == new_order["size"] and item["color"] == new_order["color"]:
            item["quantity"] = item["quantity"] + new_order["quantity"]
            break
    else:
        order.append(new_order)

    with open(ORDER_DIR, "w") as f:
         json.dump(order, f, indent=2)

    return order