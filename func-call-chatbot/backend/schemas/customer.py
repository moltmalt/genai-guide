"""
Customer-related Pydantic models for request/response validation.

This module defines the data models used for customer authentication,
including sign-in request structures and validation.
"""

from pydantic import BaseModel


class SignInData(BaseModel):
    """
    Model representing customer sign-in request data.
    
    This model defines the structure for customer authentication requests,
    requiring email and password for user login.
    """
    email: str
    """The customer's email address for authentication"""
    password: str
    """The customer's password for authentication"""
