"""
T-shirt product Pydantic models for request/response validation.

This module defines the data models used for t-shirt product functionality,
including product request structures and validation.
"""

from pydantic import BaseModel


class TShirtRequest(BaseModel):
    """
    Model representing a t-shirt product request.
    
    This model defines the structure for t-shirt product requests, specifying
    the product name, size, and color for product queries.
    """
    name: str
    """The name of the t-shirt product to search for"""
    size: str
    """The size of the t-shirt variant"""
    color: str
    """The color of the t-shirt variant"""

