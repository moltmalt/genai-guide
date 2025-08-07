"""
Shopping cart data layer functions for cart management.

This module provides functions for managing user shopping carts, including
adding items, updating quantities, deleting items, and retrieving cart contents.
All functions require user authentication via access tokens.
"""

from supabase_client import get_supabase_client
from routers.middleware import KnownAppError


def add_to_cart(*, variant_id, quantity, access_token):
    """
    Adds a product variant to the user's cart. Creates a new cart if one doesn't exist.
    This follows the proper schema where cart items reference product variants.

    Args:
        variant_id (str): The ID of the product variant to add.
        quantity (int): The quantity of the product to add.
        access_token (str): User's access token for authentication.

    Returns:
        dict: The created or updated cart item with product details.
        
    Raises:
        KnownAppError: If user is not authenticated (401), product not found (404),
                      insufficient stock (400), or database operation fails (500)
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
        
        # Check product variant exists and get stock information
        variant_response = (
            client
            .table("product_variant")
            .select("variant_id, name, size, color, price, stock")
            .eq("variant_id", variant_id)
            .execute()
        )
        
        if not variant_response.data:
            raise KnownAppError("Product variant not found", status_code=404)
        
        variant = variant_response.data[0]
        available_stock = variant["stock"]
        
        # Validate stock availability
        if quantity > available_stock:
            raise KnownAppError(
                f"Insufficient stock. Available: {available_stock}, Requested: {quantity}",
                status_code=400
            )
        
        # Get or create user's active cart
        cart_response = (
            client
            .table("cart")
            .select("cart_id, status")
            .eq("customer_id", user_id)
            .eq("status", "active")
            .execute()
        )
        
        if not cart_response.data:
            # Create new active cart for user
            cart_data = {
                "customer_id": user_id,
                "status": "active"
            }
            
            cart_create_response = (
                client
                .table("cart")
                .insert(cart_data)
                .execute()
            )
            
            if not cart_create_response.data:
                raise KnownAppError("Failed to create cart", status_code=500)
            
            cart_id = cart_create_response.data[0]["cart_id"]
        else:
            cart_id = cart_response.data[0]["cart_id"]
        
        # Check if item already exists in cart
        existing_item_response = (
            client
            .table("cart_item")
            .select("cart_item_id, quantity")
            .eq("cart_id", cart_id)
            .eq("variant_id", variant_id)
            .execute()
        )
        
        if existing_item_response.data:
            # Update existing cart item quantity
            existing_item = existing_item_response.data[0]
            new_quantity = existing_item["quantity"] + quantity
            
            # Validate stock for updated quantity
            if new_quantity > available_stock:
                raise KnownAppError(
                    f"Insufficient stock for updated quantity. Available: {available_stock}, Requested: {new_quantity}",
                    status_code=400
                )
            
            update_response = (
                client
                .table("cart_item")
                .update({"quantity": new_quantity})
                .eq("cart_item_id", existing_item["cart_item_id"])
                .execute()
            )
            
            if not update_response.data:
                raise KnownAppError("Failed to update cart item", status_code=500)
            
            return update_response.data[0]
        else:
            # Create new cart item
            cart_item_data = {
                "cart_id": cart_id,
                "variant_id": variant_id,
                "quantity": quantity
            }
            
            cart_item_response = (
                client
                .table("cart_item")
                .insert(cart_item_data)
                .execute()
            )
            
            if not cart_item_response.data:
                raise KnownAppError("Failed to add item to cart", status_code=500)
            
            return cart_item_response.data[0]
        
    except Exception as e:
        if isinstance(e, KnownAppError):
            raise e
        raise KnownAppError(f"Failed to add item to cart: {e}", status_code=500)


def get_cart_items(access_token):
    """
    Retrieve all cart items for the authenticated user.
    
    Args:
        access_token (str): User's access token for authentication.
        
    Returns:
        list: A list of dictionaries containing cart item information.
              Each dictionary includes product details like name, size, color, price, etc.
              Returns empty list if no cart items found.
              
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
    
    # Get all carts for the user
    cart_response = (
        client
        .table("cart")
        .select("cart_id")
        .eq("customer_id", user_id)
        .execute()
    )
    
    if not cart_response.data:
        return []
    
    cart_ids = [cart["cart_id"] for cart in cart_response.data]
    
    if not cart_ids:
        return []
    
    # Get all cart items with product details
    response = (
        client
        .table("cart_item")
        .select("cart_item_id, cart_id, variant_id, quantity, product_variant(name, size, color, price, stock, image_url)")
        .execute()
    )
    
    # Debug logging for image URLs
    print("Raw database response for cart items:")
    for item in response.data:
        if item.get("product_variant"):
            product = item["product_variant"]
            print(f"  Product: {product.get('name')} - image_url: {product.get('image_url')}")
    
    # Filter cart items for this user and format response
    cart_items = []
    for item in response.data:
        if item.get("cart_id") in cart_ids:
            product = item["product_variant"]
            cart_item = {
                "id": item["cart_item_id"], 
                "cart_item_id": item["cart_item_id"],
                "cart_id": item["cart_id"], 
                "name": product["name"],
                "size": product["size"],
                "color": product["color"],
                "price": product["price"],
                "quantity": item["quantity"],
                "stock": product["stock"],
                "image_url": product.get("image_url")
            }
            print(f"Cart item for {product['name']}: image_url = {product.get('image_url')}")
            cart_items.append(cart_item)
    
    return cart_items


def update_cart_item(*, cart_item_id, quantity, access_token):
    """
    Update the quantity of a specific cart item.
    
    Args:
        cart_item_id (str): The ID of the cart item to update.
        quantity (int): The new quantity for the cart item.
        access_token (str): User's access token for authentication.
        
    Returns:
        dict: The updated cart item data.
        
    Raises:
        KnownAppError: If cart item not found (404), insufficient stock (400),
                      or database operation fails (500)
    """
    client = get_supabase_client(access_token=access_token)
    try:
        # Get current cart item information
        cart_item_response = (
            client
            .table("cart_item")
            .select("variant_id, quantity")
            .eq("cart_item_id", cart_item_id)
            .execute()
        )
        
        if not cart_item_response.data:
            raise KnownAppError("Cart item not found", status_code=404)
        
        cart_item = cart_item_response.data[0]
        variant_id = cart_item["variant_id"]
        current_quantity = cart_item["quantity"]
        
        # Get product variant stock information
        variant_response = (
            client
            .table("product_variant")
            .select("name, size, color, stock")
            .eq("variant_id", variant_id)
            .execute()
        )
        
        if not variant_response.data:
            raise KnownAppError("Product variant not found", status_code=404)
        
        variant = variant_response.data[0]
        available_stock = variant["stock"]
        
        # Calculate if we have enough stock
        # Account for the current quantity in cart (subtract it from available stock)
        # since the user might be reducing the quantity
        stock_needed = quantity - current_quantity
        
        if stock_needed > 0 and stock_needed > available_stock:
            raise KnownAppError(
                f"Not enough stock available. Requested: {quantity}, Available: {available_stock + current_quantity}",
                status_code=400
            )
        
        # Update the quantity
        response = (
            client
            .table("cart_item")
            .update({"quantity": quantity})
            .eq("cart_item_id", cart_item_id)
            .execute()
        )
        return response.data
    except Exception as e:
        if isinstance(e, KnownAppError):
            raise e
        raise KnownAppError(f"Failed to update cart item: {e}", status_code=500)


def delete_cart_item(*, cart_item_id, access_token):
    """
    Delete a specific cart item from the user's cart.
    
    Args:
        cart_item_id (str): The ID of the cart item to delete.
        access_token (str): User's access token for authentication.
        
    Returns:
        dict: The deleted cart item data.
        
    Raises:
        KnownAppError: If database operation fails (500 status code)
    """
    client = get_supabase_client(access_token=access_token)
    try:
        # Delete the cart item
        response = (
            client
            .table("cart_item")
            .delete()
            .eq("cart_item_id", cart_item_id)
            .execute()
        )
        return response.data
    except Exception as e:
        raise KnownAppError(f"Failed to delete cart item: {e}", status_code=500)


def get_user_cart(access_token):
    """
    Get the complete cart information for the authenticated user.
    
    Args:
        access_token (str): User's access token for authentication.
        
    Returns:
        dict or None: A dictionary containing cart information with items list.
                     Returns None if no cart exists for the user.
                     
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

    # First try to get active cart
    cart_response = (
        client
        .table("cart")
        .select("cart_id, status")
        .eq("customer_id", user_id)
        .eq("status", "active")
        .execute()
    )
    
    # If no active cart, get the most recent cart
    if not cart_response.data:
        cart_response = (
            client
            .table("cart")
            .select("cart_id, status")
            .eq("customer_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    
    if not cart_response.data:
        return None
        
    cart = cart_response.data[0]
    cart_id = cart["cart_id"]
    
    # Get cart items with product details
    items_response = (
        client
        .table("cart_item")
        .select("cart_item_id, variant_id, quantity, product_variant(name, size, color, price, stock)")
        .eq("cart_id", cart_id)
        .execute()
    )
    
    # Flatten the items for frontend compatibility
    items = []
    for item in items_response.data:
        product = item["product_variant"]
        items.append({
            "id": item["cart_item_id"],
            "cart_item_id": item["cart_item_id"],
            "cart_id": cart_id, 
            "name": product["name"],
            "size": product["size"],
            "color": product["color"],
            "price": product["price"],
            "quantity": item["quantity"],
            "stock": product["stock"]
        })
    
    cart["items"] = items
    return cart