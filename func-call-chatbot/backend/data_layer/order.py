"""
Order management data layer functions for order processing.

This module provides functions for managing customer orders, including
placing orders, updating order status, managing order items, and retrieving
order history. All functions require user authentication via access tokens.
"""

from supabase_client import get_supabase_client
from routers.middleware import KnownAppError


def place_order(*, access_token):
    """
    Places an order by converting the user's active cart items into an order.
    This follows the proper schema where orders are created from cart items.

    Args:
        access_token (str): User's access token for authentication.

    Returns:
        dict: The created order with its items.
        
    Raises:
        KnownAppError: If user is not authenticated (401), no active cart found (404),
                      cart is empty (400), or database operation fails (500)
    """
    client = get_supabase_client(access_token=access_token)
    
    try:
        # Get authenticated user ID
        user = client.auth.get_user()
        if not user or not hasattr(user, "user") or not user.user:
            session = client.auth.get_session()
            if not session or not session.user:
                raise KnownAppError("User not authenticated", status_code=401)
            user_id = session.user.id
        else:
            user_id = user.user.id
        
        # Get user's active cart
        cart_response = (
            client
            .table("cart")
            .select("cart_id, status")
            .eq("customer_id", user_id)
            .eq("status", "active")
            .execute()
        )
        
        if not cart_response.data:
            raise KnownAppError("No active cart found", status_code=404)
        
        cart = cart_response.data[0]
        cart_id = cart["cart_id"]
        
        # Get cart items with product details
        cart_items_response = (
            client
            .table("cart_item")
            .select("cart_item_id, variant_id, quantity, product_variant(name, size, color, price, stock)")
            .eq("cart_id", cart_id)
            .execute()
        )
        
        if not cart_items_response.data:
            raise KnownAppError("Cart is empty", status_code=400)
        
        cart_items = cart_items_response.data
        
        # Calculate total amount
        total_amount = 0
        for item in cart_items:
            product = item["product_variant"]
            total_amount += float(product["price"]) * item["quantity"]
        
        # Create the order
        order_data = {
            "customer_id": user_id,
            "cart_id": cart_id,
            "order_date": "now()",  
            "status": "pending",
            "total_amount": total_amount
        }
        
        order_response = (
            client
            .table("order")
            .insert(order_data)
            .execute()
        )
        
        if not order_response.data:
            raise KnownAppError("Failed to create order", status_code=500)
        
        order = order_response.data[0]
        order_id = order["order_id"]
        
        # Create order items from cart items
        order_items = []
        for cart_item in cart_items:
            product = cart_item["product_variant"]
            order_item_data = {
                "order_id": order_id,
                "variant_id": cart_item["variant_id"],
                "quantity": cart_item["quantity"],
                "item_price": float(product["price"])
            }
            
            order_item_response = (
                client
                .table("order_item")
                .insert(order_item_data)
                .execute()
            )
            
            if order_item_response.data:
                order_items.append(order_item_response.data[0])
        
        # Update cart status to "ordered"
        (
            client
            .table("cart")
            .update({"status": "ordered"})
            .eq("cart_id", cart_id)
            .execute()
        )
        
        # Delete all cart items since they've been converted to order items
        (
            client
            .table("cart_item")
            .delete()
            .eq("cart_id", cart_id)
            .execute()
        )
        
        order["items"] = order_items
        return order
        
    except Exception as e:
        if isinstance(e, KnownAppError):
            raise e
        raise KnownAppError(f"Failed to place order: {e}", status_code=500)


def update_order(*, order_id, status, total_amount, access_token):
    """
    Update the status and total amount of an order.
    
    Args:
        order_id (str): The ID of the order to update.
        status (str): The new status for the order.
        total_amount (float): The new total amount for the order.
        access_token (str): User's access token for authentication.
        
    Returns:
        dict: The updated order data.
        
    Raises:
        KnownAppError: If database operation fails (500 status code)
    """
    client = get_supabase_client(access_token=access_token)
    try:
        # Update order status and total amount
        response = (
            client
            .table("order")
            .update({"status": status, "total_amount": total_amount})
            .eq("order_id", order_id)
            .execute()
        )
        return response.data
    except Exception as e:
        raise KnownAppError(f"Failed to update order: {e}", status_code=500)


def delete_order(*, order_id, access_token):
    """
    Delete an order by its ID.
    
    Args:
        order_id (str): The ID of the order to delete.
        access_token (str): User's access token for authentication.
        
    Returns:
        dict: The deleted order data.
        
    Raises:
        KnownAppError: If database operation fails (500 status code)
    """
    client = get_supabase_client(access_token=access_token)
    try:
        # Delete the order
        response = (
            client
            .table("order")
            .delete()
            .eq("order_id", order_id)
            .execute()
        )
        return response.data
    except Exception as e:
        raise KnownAppError(f"Failed to delete order: {e}", status_code=500)


def update_order_item(*, order_item_id, quantity, item_price, access_token):
    """
    Update the quantity and price of an order item.
    
    Args:
        order_item_id (str): The ID of the order item to update.
        quantity (int): The new quantity for the order item.
        item_price (float): The new price for the order item.
        access_token (str): User's access token for authentication.
        
    Returns:
        dict: The updated order item data.
        
    Raises:
        KnownAppError: If order item not found (404) or database operation fails (500)
    """
    client = get_supabase_client(access_token=access_token)
    try:
        # Update the order item
        response = (
            client
            .table("order_item")
            .update({"quantity": quantity, "item_price": item_price})
            .eq("order_item_id", order_item_id)
            .execute()
        )
        
        if not response.data:
            raise KnownAppError("Order item not found", status_code=404)
        
        # Get the order_id for this item
        order_item_response = (
            client
            .table("order_item")
            .select("order_id")
            .eq("order_item_id", order_item_id)
            .execute()
        )
        
        if not order_item_response.data:
            raise KnownAppError("Order item not found", status_code=404)
        
        order_id = order_item_response.data[0]["order_id"]
        
        # Recalculate total amount for the order
        order_items_response = (
            client
            .table("order_item")
            .select("quantity, item_price")
            .eq("order_id", order_id)
            .execute()
        )
        
        total_amount = 0
        for item in order_items_response.data:
            total_amount += float(item["item_price"]) * item["quantity"]
        
        # Update the order with new total
        (
            client
            .table("order")
            .update({"total_amount": total_amount})
            .eq("order_id", order_id)
            .execute()
        )
        
        return response.data
    except Exception as e:
        raise KnownAppError(f"Failed to update order item: {e}", status_code=500)


def delete_order_item(*, order_item_id, access_token):
    """
    Delete an order item by its ID.
    
    Args:
        order_item_id (str): The ID of the order item to delete.
        access_token (str): User's access token for authentication.
        
    Returns:
        dict: The deleted order item data.
        
    Raises:
        KnownAppError: If order item not found (404) or database operation fails (500)
    """
    client = get_supabase_client(access_token=access_token)
    try:
        # Get the order_id before deleting the item
        order_item_response = (
            client
            .table("order_item")
            .select("order_id")
            .eq("order_item_id", order_item_id)
            .execute()
        )
        
        if not order_item_response.data:
            raise KnownAppError("Order item not found", status_code=404)
        
        order_id = order_item_response.data[0]["order_id"]
        
        # Delete the order item
        response = (
            client
            .table("order_item")
            .delete()
            .eq("order_item_id", order_item_id)
            .execute()
        )
        
        # Recalculate total amount for the order
        order_items_response = (
            client
            .table("order_item")
            .select("quantity, item_price")
            .eq("order_id", order_id)
            .execute()
        )
        
        total_amount = 0
        for item in order_items_response.data:
            total_amount += float(item["item_price"]) * item["quantity"]
        
        # Update the order with new total
        (
            client
            .table("order")
            .update({"total_amount": total_amount})
            .eq("order_id", order_id)
            .execute()
        )
        
        return response.data
    except Exception as e:
        raise KnownAppError(f"Failed to delete order item: {e}", status_code=500)


def get_user_orders(access_token):
    """
    Get all orders for the authenticated user, including their items.
    
    Args:
        access_token (str): User's access token for authentication.
        
    Returns:
        list: A list of dictionaries containing order information with items.
              Each order includes order details and a list of order items.
              Returns empty list if no orders found.
              
    Raises:
        KnownAppError: If user is not authenticated (401 status code)
    """
    client = get_supabase_client(access_token=access_token)
    try:
        # Get authenticated user ID
        user = client.auth.get_user()
        if not user or not hasattr(user, "user") or not user.user:
            session = client.auth.get_session()
            if not session or not session.user:
                raise KnownAppError("User not authenticated", status_code=401)
            user_id = session.user.id
        else:
            user_id = user.user.id
    except Exception as e:
        raise KnownAppError("User not authenticated", status_code=401)

    # Get all orders for the user, ordered by date (newest first)
    orders_response = (
        client
        .table("order")
        .select("order_id, cart_id, order_date, status, total_amount")
        .eq("customer_id", user_id)
        .order("order_date", desc=True)
        .execute()
    )
    
    orders = orders_response.data or []
    
    # Get order items for each order
    for order in orders:
        order_id = order["order_id"]
        items_response = (
            client
            .table("order_item")
            .select("order_item_id, variant_id, quantity, item_price, product_variant(name, size, color, price, stock)")
            .eq("order_id", order_id)
            .execute()
        )
        
        # Flatten the items for frontend compatibility
        items = []
        for item in items_response.data:
            product = item["product_variant"]
            items.append({
                "id": item["order_item_id"],
                "order_item_id": item["order_item_id"],
                "name": product["name"],
                "size": product["size"],
                "color": product["color"],
                "price": item["item_price"],  
                "quantity": item["quantity"],
                "stock": product["stock"]
            })
        
        order["items"] = items
    return orders