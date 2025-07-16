from func import get_t_shirt, add_to_cart, place_order

class TShirtDatabase:
    """
    Handles t-shirt database operations such as retrieving t-shirts, adding to cart, and placing orders.
    """
    def __init__(self):
        """
        Initializes the TShirtDatabase with a function map for database operations.
        """
        self.function_map = {
            "get_t_shirts": get_t_shirt,
            "add_to_cart": add_to_cart,
            "place_order": place_order
        }

    def get_t_shirts(self, name, size, color):
        """
        Retrieves t-shirts matching the given name, size, and color.

        Args:
            name (str): The name of the t-shirt.
            size (str): The size of the t-shirt.
            color (str): The color of the t-shirt.

        Returns:
            dict or str: The matching t-shirt(s) or a message if not found.
        """
        return self.function_map["get_t_shirts"](name=name, size=size, color=color)
    
    def add_to_cart(self, name, size, color, price, quantity):
        """
        Adds a t-shirt to the cart or updates the quantity if it already exists.

        Args:
            name (str): The name of the t-shirt.
            size (str): The size of the t-shirt.
            color (str): The color of the t-shirt.
            price (str or float): The price of the t-shirt.
            quantity (int): The quantity to add.

        Returns:
            list: The updated cart.
        """
        return self.function_map["add_to_cart"](
            name=name, 
            size=size, 
            color=color, 
            price=price,
            quantity=quantity, 
        )
    
    def place_order(self, name, size, color, price, quantity):
        """
        Places an order for a t-shirt or updates the quantity if it already exists in the order list.

        Args:
            name (str): The name of the t-shirt.
            size (str): The size of the t-shirt.
            color (str): The color of the t-shirt.
            price (str or float): The price of the t-shirt.
            quantity (int): The quantity to order.

        Returns:
            list: The updated order list.
        """
        return self.function_map["place_order"](
            name=name, 
            size=size, 
            color=color, 
            price=price,
            quantity=quantity
        )