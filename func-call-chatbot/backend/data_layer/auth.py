"""
Authentication data layer functions for user management.

This module provides functions for user authentication, including sign-in,
sign-out, and user ID retrieval operations using Supabase authentication.
"""

from supabase_client import get_supabase_client, get_access_token
from fastapi import HTTPException, Request
from routers.middleware import KnownAppError


def sign_in(email: str, password: str):
    """
    Authenticate a user with email and password.
    
    Args:
        email (str): The user's email address
        password (str): The user's password
        
    Returns:
        dict: A dictionary containing authentication tokens and user information
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
    # Attempt to sign in the user with provided credentials
    response = (
        get_supabase_client()
        .auth
        .sign_in_with_password({
            "email": email,
            "password": password
        })
    )

    # Check if authentication was successful
    if response.user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Return authentication tokens and user information
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user": {
            "id": response.user.id,
            "email": response.user.email
        }
    }


def sign_out(request: Request):
    """
    Sign out the currently authenticated user.
    
    Args:
        request (Request): FastAPI request object containing authentication headers
        
    Returns:
        dict: Response data from the sign-out operation
        
    Raises:
        KnownAppError: If user is not authenticated
    """
    # Extract access token from request headers
    access_token = get_access_token(request)
    
    # Perform sign-out operation
    response = (
        get_supabase_client(access_token=access_token)
        .auth
        .sign_out()
    )
    return response.data


def get_user_id(access_token=None):
    """
    Get the user ID of the currently authenticated user.
    
    Args:
        access_token (str, optional): Access token for authentication. 
                                    If not provided, uses default client.
        
    Returns:
        str: The authenticated user's ID
        
    Raises:
        KnownAppError: If user is not authenticated (401 status code)
    """
    # Initialize Supabase client with or without access token
    if access_token:
        client = get_supabase_client(access_token=access_token)
    else:
        client = get_supabase_client()
    
    # Get current user information
    user = client.auth.get_user()
    
    # Validate that user is authenticated
    if not user or not hasattr(user, "user") or not user.user:
        raise KnownAppError("User not authenticated", status_code=401)
    
    # Extract and return user ID
    user_id = user.user.id
    return user_id
