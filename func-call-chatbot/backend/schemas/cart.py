"""
Cart-related Pydantic models for request/response validation.

This module defines the data models used for shopping cart functionality,
including cart item structures and validation.
"""

from decimal import Decimal
from pydantic import BaseModel


class CartItem(BaseModel):
    """
    Model representing a cart item for adding products to cart.
    
    This model defines the structure for cart item requests, specifying
    which product variant to add and in what quantity.
    """
    variant_id: str
    """The unique identifier of the product variant to add to cart"""
    quantity: int
    """The quantity of the product variant to add to cart"""

