"""
Wishlist data layer functions for wishlist management.

This module provides functions for managing user wishlists, including
adding items, removing items, and retrieving wishlist contents.
All functions require user authentication via access tokens.
"""

from supabase_client import get_supabase_client
from routers.middleware import KnownAppError


def add_to_wishlist(*, variant_id, access_token):
    """
    Adds a product variant to the user's wishlist.
    
    Args:
        variant_id (str): The ID of the product variant to add
        access_token (str): User's access token for authentication
        
    Returns:
        dict: The created wishlist item with product details
        
    Raises:
        KnownAppError: If user is not authenticated (401), item already in wishlist (400),
                      or database operation fails (500)
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
        
        # Check if item already exists in wishlist
        existing_response = (
            client
            .table("wishlist")
            .select("id")
            .eq("customer_id", user_id)
            .eq("variant_id", variant_id)
            .execute()
        )
        
        if existing_response.data:
            raise KnownAppError("Item already in wishlist", status_code=400)
        
        # Add item to wishlist
        wishlist_data = {
            "customer_id": user_id,
            "variant_id": variant_id
        }
        
        response = (
            client
            .table("wishlist")
            .insert(wishlist_data)
            .execute()
        )
        
        if not response.data:
            raise KnownAppError("Failed to add item to wishlist", status_code=500)
        
        return response.data[0]
        
    except Exception as e:
        if isinstance(e, KnownAppError):
            raise e
        raise KnownAppError(f"Failed to add item to wishlist: {e}", status_code=500)


def remove_from_wishlist(*, variant_id, access_token):
    """
    Removes a product variant from the user's wishlist.
    
    Args:
        variant_id (str): The ID of the product variant to remove
        access_token (str): User's access token for authentication
        
    Returns:
        dict: The deleted wishlist item data
        
    Raises:
        KnownAppError: If user is not authenticated (401), item not found in wishlist (404),
                      or database operation fails (500)
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
        
        # Remove item from wishlist
        response = (
            client
            .table("wishlist")
            .delete()
            .eq("customer_id", user_id)
            .eq("variant_id", variant_id)
            .execute()
        )
        
        if not response.data:
            raise KnownAppError("Item not found in wishlist", status_code=404)
        
        return response.data[0]
        
    except Exception as e:
        if isinstance(e, KnownAppError):
            raise e
        raise KnownAppError(f"Failed to remove item from wishlist: {e}", status_code=500)


def get_wishlist_items(access_token):
    """
    Gets all wishlist items for the authenticated user.
    
    Args:
        access_token (str): User's access token for authentication
        
    Returns:
        list: List of wishlist items with product details.
              Each item includes product information like name, size, color, price, etc.
              Returns empty list if no wishlist items found.
              
    Raises:
        KnownAppError: If user is not authenticated (401) or database operation fails (500)
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
        
        # Get wishlist items with product details
        response = (
            client
            .table("wishlist")
            .select("id, created_at, variant_id, product_variant(name, size, color, price, stock, image_url)")
            .eq("customer_id", user_id)
            .execute()
        )
        
        # Format wishlist items for frontend compatibility
        wishlist_items = []
        for item in response.data:
            product = item["product_variant"]
            wishlist_items.append({
                "id": item["id"],
                "created_at": item["created_at"],
                "variant_id": item["variant_id"],
                "name": product["name"],
                "size": product["size"],
                "color": product["color"],
                "price": product["price"],
                "stock": product["stock"],
                "image_url": product.get("image_url")
            })
        
        return wishlist_items
        
    except Exception as e:
        if isinstance(e, KnownAppError):
            raise e
        raise KnownAppError(f"Failed to get wishlist items: {e}", status_code=500) 