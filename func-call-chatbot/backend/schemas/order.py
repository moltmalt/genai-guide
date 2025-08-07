"""
Order-related Pydantic models for request/response validation.

This module defines the data models used for order processing,
including order request structures and validation.
"""

from pydantic import BaseModel
from decimal import Decimal


class OrderRequest(BaseModel):
    """
    Model representing an order request for product purchases.
    
    This model defines the structure for order requests, specifying
    the product details and quantity for purchase.
    """
    name: str
    """The name of the product to order"""
    quantity: int
    """The quantity of the product to order"""
    size: str
    """The size of the product variant"""
    color: str
    """The color of the product variant"""
    price: Decimal
    """The price of the product variant (using Decimal for precision)"""