"""
T-shirt product data layer functions for inventory management.

This module provides functions for retrieving t-shirt products from the database,
including getting all shirts and finding specific shirts by name, size, and color.
"""

from supabase_client import get_supabase_client
from routers.middleware import KnownAppError


def get_all_shirts():
    """
    Retrieve all t-shirt variants from the database.
    
    Returns:
        list: A list of dictionaries containing all t-shirt product variants
              Each dictionary contains product information like name, size, color, price, stock, etc.
              
    Raises:
        KnownAppError: If database query fails (500 status code)
    """
    try:
        # Query all product variants from the database
        response = (
            get_supabase_client()
            .table("product_variant")
            .select("*")
            .execute()
        )
        return response.data
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)


def get_t_shirt(name, size, color):
    """
    Retrieves a t-shirt from the database matching the given name, size, and color.
    This function is case-insensitive for all parameters.

    Args:
        name (str): The name of the t-shirt (supports partial matching)
        size (str): The size of the t-shirt (supports partial matching)
        color (str): The color of the t-shirt (supports partial matching)

    Returns:
        list: A list of dictionaries containing matching t-shirt variants.
              Each dictionary contains product information like name, size, color, price, stock, etc.
              Returns empty list if no matches found.

    Raises:
        KnownAppError: If database query fails (500 status code)
    """
    try:
        # Query product variants with case-insensitive partial matching
        response = (
            get_supabase_client()
            .table("product_variant")
            .select("*")
            .ilike("name", f"%{name}%")
            .ilike("size", f"%{size}%")
            .ilike("color", f"%{color}%")
            .execute()
        )
        return response.data
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

