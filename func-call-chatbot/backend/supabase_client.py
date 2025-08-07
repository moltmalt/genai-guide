import os

from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi import Depends, Request
from routers.middleware import KnownAppError
from core.config import settings

load_dotenv(override=True)

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client(access_token=None):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)    
    if access_token:
        try:
            client.auth.set_session(access_token, access_token)
            print("Session set successfully with set_session")
        except Exception as e:
            print(f"Error setting session: {e}")
            print("Warning: Could not set authentication, proceeding without auth")
            try:
                client.auth.session = {
                    "access_token": access_token,
                    "refresh_token": access_token,
                    "expires_at": None
                }
                print("Session set successfully with manual assignment")
            except Exception as e2:
                print(f"Alternative auth method also failed: {e2}")
                try:
                    client.auth.session = {"access_token": access_token}
                    print("Session set successfully with minimal assignment")
                except Exception as e3:
                    print(f"Final auth fallback also failed: {e3}")
                    try:
                        client.auth.access_token = access_token
                        print("Access token set directly")
                    except Exception as e4:
                        print(f"Direct token setting also failed: {e4}")
    
    try:
        test_query = client.table("product_variant").select("*").limit(1)
        print(f"Test query created successfully: {type(test_query)}")
    except Exception as e:
        print(f"Test query failed: {e}")
    
    return client

def get_access_token(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise KnownAppError("Missing or invalid authorization header", status_code=401)
    return auth_header.split(" ")[1]


