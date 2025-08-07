"""
Database model for centralized database operations.

This module provides a Database class that acts as a facade for all database operations,
including product management, cart operations, order processing, and wishlist management.
It wraps functions from the data layer to provide a clean, unified interface.
"""

from data_layer.tshirt import get_t_shirt, get_all_shirts
from data_layer.order import place_order, update_order, delete_order, update_order_item, delete_order_item, get_user_orders
from data_layer.cart import add_to_cart, get_cart_items, update_cart_item, delete_cart_item, get_user_cart
from data_layer.wishlist import add_to_wishlist, remove_from_wishlist, get_wishlist_items


class Database:
    """
    Database model class for handling all database operations.
    
    This class provides a unified interface for all database operations including
    product retrieval, cart management, order processing, and wishlist operations.
    It acts as a facade that wraps functions from the data layer.
    """
    
    def __init__(self):
        """
        Initialize the Database model with function mappings.
        
        Sets up a function map that maps method names to their corresponding
        data layer functions for all database operations.
        """
        self.function_map = {
            "get_t_shirts": get_t_shirt,
            "add_to_cart": add_to_cart,
            "place_order": place_order,
            "get_all_shirts": get_all_shirts,
            "get_cart_items": get_cart_items,
            "add_to_wishlist": add_to_wishlist,
            "remove_from_wishlist": remove_from_wishlist,
            "get_wishlist_items": get_wishlist_items,
            "update_cart_item": update_cart_item,
            "delete_cart_item": delete_cart_item,
            "update_order": update_order,
            "delete_order": delete_order,
            "update_order_item": update_order_item,
            "delete_order_item": delete_order_item,
            "get_user_cart": get_user_cart,
            "get_user_orders": get_user_orders
        }

    def get_all_shirts(self):
        """
        Retrieves all available t-shirt variants from the database.

        Returns:
            list: List of all t-shirt variants with product details.
                  Each item contains name, size, color, price, stock, etc.
                  
        Raises:
            KnownAppError: If database query fails (500 status code)
        """
        return self.function_map["get_all_shirts"]()

    def get_t_shirt(self, name, size, color):
        """
        Retrieves t-shirts matching the given name, size, and color.
        Supports case-insensitive partial matching for all parameters.

        Args:
            name (str): The name of the t-shirt (supports partial matching)
            size (str): The size of the t-shirt (supports partial matching)
            color (str): The color of the t-shirt (supports partial matching)

        Returns:
            list: List of matching t-shirt variants with product details.
                  Returns empty list if no matches found.
                  
        Raises:
            KnownAppError: If database query fails (500 status code)
        """
        return self.function_map["get_t_shirts"](name=name, size=size, color=color)
    
    def get_cart_items(self, access_token=None):
        """
        Retrieves cart items for the authenticated user.

        Args:
            access_token (str, optional): User's access token for authentication.
                                        Required for authenticated operations.

        Returns:
            list: List of cart items with product details.
                  Each item includes name, size, color, price, quantity, etc.
                  Returns empty list if no cart items found.
                  
        Raises:
            KnownAppError: If user is not authenticated (401 status code)
        """
        return self.function_map["get_cart_items"](access_token=access_token)
    
    def add_to_cart(self, variant_id, quantity, access_token):
        """
        Adds a t-shirt variant to the user's cart with stock validation.

        Args:
            variant_id (str): The variant ID of the t-shirt to add
            quantity (int): The quantity to add to the cart
            access_token (str): User's access token for authentication

        Returns:
            dict: The created or updated cart item with product details
            
        Raises:
            KnownAppError: If user is not authenticated (401), product not found (404),
                          insufficient stock (400), or database operation fails (500)
        """
        return self.function_map["add_to_cart"](
            variant_id=variant_id,
            quantity=quantity,
            access_token=access_token
        )
    
    def place_order(self, access_token):
        """
        Places an order by converting the user's active cart items into an order.

        Args:
            access_token (str): User's access token for authentication

        Returns:
            dict: The created order with its items and total amount
            
        Raises:
            KnownAppError: If user is not authenticated (401), no active cart found (404),
                          cart is empty (400), or database operation fails (500)
        """
        return self.function_map["place_order"](access_token=access_token)

    def update_cart_item(self, cart_item_id, quantity, access_token):
        """
        Updates the quantity of a specific cart item with stock validation.

        Args:
            cart_item_id (str): The cart item ID to update
            quantity (int): The new quantity for the cart item
            access_token (str): User's access token for authentication

        Returns:
            dict: The updated cart item data
            
        Raises:
            KnownAppError: If cart item not found (404), insufficient stock (400),
                          or database operation fails (500)
        """
        return self.function_map["update_cart_item"](
            cart_item_id=cart_item_id, 
            quantity=quantity, 
            access_token=access_token
        )

    def delete_cart_item(self, cart_item_id, access_token):
        """
        Deletes a specific cart item from the user's cart.

        Args:
            cart_item_id (str): The cart item ID to delete
            access_token (str): User's access token for authentication

        Returns:
            dict: The deleted cart item data
            
        Raises:
            KnownAppError: If database operation fails (500 status code)
        """
        return self.function_map["delete_cart_item"](
            cart_item_id=cart_item_id, 
            access_token=access_token
        )

    def update_order(self, order_id, status, total_amount, access_token):
        """
        Updates an order's status and total amount.

        Args:
            order_id (str): The order ID to update
            status (str): The new status for the order
            total_amount (float): The new total amount for the order
            access_token (str): User's access token for authentication

        Returns:
            dict: The updated order data
            
        Raises:
            KnownAppError: If database operation fails (500 status code)
        """
        return self.function_map["update_order"](
            order_id=order_id, 
            status=status, 
            total_amount=total_amount, 
            access_token=access_token
        )

    def delete_order(self, order_id, access_token):
        """
        Deletes an order by its ID.

        Args:
            order_id (str): The order ID to delete
            access_token (str): User's access token for authentication

        Returns:
            dict: The deleted order data
            
        Raises:
            KnownAppError: If database operation fails (500 status code)
        """
        return self.function_map["delete_order"](
            order_id=order_id, 
            access_token=access_token
        )

    def update_order_item(self, order_item_id, quantity, item_price, access_token):
        """
        Updates an order item's quantity and price, recalculating order total.

        Args:
            order_item_id (str): The order item ID to update
            quantity (int): The new quantity for the order item
            item_price (float): The new price for the order item
            access_token (str): User's access token for authentication

        Returns:
            dict: The updated order item data
            
        Raises:
            KnownAppError: If order item not found (404) or database operation fails (500)
        """
        return self.function_map["update_order_item"](
            order_item_id=order_item_id, 
            quantity=quantity, 
            item_price=item_price, 
            access_token=access_token
        )

    def delete_order_item(self, order_item_id, access_token):
        """
        Deletes an order item and recalculates the order total.

        Args:
            order_item_id (str): The order item ID to delete
            access_token (str): User's access token for authentication

        Returns:
            dict: The deleted order item data
            
        Raises:
            KnownAppError: If order item not found (404) or database operation fails (500)
        """
        return self.function_map["delete_order_item"](
            order_item_id=order_item_id, 
            access_token=access_token
        )

    def get_user_cart(self, access_token):
        """
        Gets the complete cart information for the authenticated user.

        Args:
            access_token (str): User's access token for authentication

        Returns:
            dict or None: A dictionary containing cart information with items list.
                         Returns None if no cart exists for the user.
                         
        Raises:
            KnownAppError: If user is not authenticated (401 status code)
        """
        return self.function_map["get_user_cart"](access_token=access_token)

    def get_user_orders(self, access_token):
        """
        Gets all orders for the authenticated user, including their items.

        Args:
            access_token (str): User's access token for authentication

        Returns:
            list: A list of dictionaries containing order information with items.
                  Each order includes order details and a list of order items.
                  Returns empty list if no orders found.
                  
        Raises:
            KnownAppError: If user is not authenticated (401 status code)
        """
        return self.function_map["get_user_orders"](access_token=access_token)

    def add_to_wishlist(self, variant_id, access_token):
        """
        Adds a t-shirt variant to the user's wishlist with duplicate checking.

        Args:
            variant_id (str): The variant ID of the t-shirt to add
            access_token (str): User's access token for authentication

        Returns:
            dict: The created wishlist item with product details
            
        Raises:
            KnownAppError: If user is not authenticated (401), item already in wishlist (400),
                          or database operation fails (500)
        """
        return self.function_map["add_to_wishlist"](
            variant_id=variant_id, 
            access_token=access_token
        )

    def remove_from_wishlist(self, variant_id, access_token):
        """
        Removes a t-shirt variant from the user's wishlist.

        Args:
            variant_id (str): The variant ID of the t-shirt to remove
            access_token (str): User's access token for authentication

        Returns:
            dict: The deleted wishlist item data
            
        Raises:
            KnownAppError: If user is not authenticated (401), item not found in wishlist (404),
                          or database operation fails (500)
        """
        return self.function_map["remove_from_wishlist"](
            variant_id=variant_id, 
            access_token=access_token
        )

    def get_wishlist_items(self, access_token):
        """
        Gets all items in the user's wishlist with product details.

        Args:
            access_token (str): User's access token for authentication

        Returns:
            list: List of wishlist items with product details.
                  Each item includes product information like name, size, color, price, etc.
                  Returns empty list if no wishlist items found.
                  
        Raises:
            KnownAppError: If user is not authenticated (401) or database operation fails (500)
        """
        return self.function_map["get_wishlist_items"](access_token=access_token)