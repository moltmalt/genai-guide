"""
Customer model for user authentication operations.

This module provides a Customer class that wraps authentication functions
from the data layer, providing a clean interface for customer-related operations.
"""

from data_layer.auth import sign_in, sign_out


class Customer:
    """
    Customer model class for handling user authentication operations.
    
    This class provides a wrapper around authentication functions from the data layer,
    offering a clean interface for customer sign-in and sign-out operations.
    """
    
    def __init__(self):
        """
        Initialize the Customer model with authentication function mappings.
        
        Sets up a function map that maps method names to their corresponding
        data layer authentication functions.
        """
        self.function_map = {
            "sign_in": sign_in,
            "sign_out": sign_out
        }

    def sign_in(self, email: str, password: str):
        """
        Authenticate a customer with email and password.
        
        Args:
            email (str): The customer's email address
            password (str): The customer's password
            
        Returns:
            dict: Authentication response containing access token, refresh token, and user info
                  {
                      "access_token": str,
                      "refresh_token": str,
                      "user": {
                          "id": str,
                          "email": str
                      }
                  }
                  
        Raises:
            HTTPException: If authentication fails (401 status code)
        """
        return self.function_map["sign_in"](email, password)
    
    def sign_out(self):
        """
        Sign out the currently authenticated customer.
        
        Returns:
            dict: Response data from the sign-out operation
            
        Raises:
            KnownAppError: If user is not authenticated
        """
        return self.function_map["sign_out"]()