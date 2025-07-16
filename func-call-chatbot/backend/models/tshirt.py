from func import get_t_shirt, add_to_cart, place_order

class TShirtDatabase:
    def __init__(self):
        self.function_map = {
            "get_t_shirts": get_t_shirt,
            "add_to_cart": add_to_cart,
            "place_order": place_order
        }

    def get_t_shirts(self, name, size, color):
        return self.function_map["get_t_shirts"](name=name, size=size, color=color)
    
    def add_to_cart(self, name, size, color, price, quantity):
        return self.function_map["add_to_cart"](
            name=name, 
            size=size, 
            color=color, 
            price=price,
            quantity=quantity, 
        )
    
    def place_order(self, name, size, color, price, quantity):
        return self.function_map["place_order"](
            name=name, 
            size=size, 
            color=color, 
            price=price,
            quantity=quantity
        )