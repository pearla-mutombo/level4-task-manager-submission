"""Supabase authentication helpers for the Flask Task Manager."""

from flask import request

from httpx import RequestError

from supabase_auth.errors import AuthApiError

from supabase import create_client

from config import get_supabase_url, get_supabase_key

def get_supabase_client():
    """Create a Supabase client using our project settings."""
    return create_client(
        get_supabase_url(),
        get_supabase_key(),
    )

def get_access_token():
    """Read the Bearer token from an incoming HTTP request."""
    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        return None

    token = authorization[len("Bearer "):].strip()

    return token or None

def verify_access_token(token):
    """Ask Supabase to verify an access token."""
    client = get_supabase_client()

    try:
        response = client.auth.get_user(token)
        return response.user

    except AuthApiError:
        # Supabase rejected an invalid or expired token.
        return None

    except RequestError as error:
        # Supabase could not be reached.
        raise ConnectionError(
            "Supabase authentication service is unavailable."
        ) from error