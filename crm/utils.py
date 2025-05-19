import os
import requests
from django.core.cache import cache

# Keys for caching access token and its expiry (not used in current version, but included for reference)
ACCESS_TOKEN_CACHE_KEY = "ZOHO_ACCESS_TOKEN"
EXPIRY_CACHE_KEY = "ZOHO_ACCESS_TOKEN_EXPIRY"

def get_access_token():
    """
    Retrieves a new Zoho access token using the stored refresh token.
    Handles missing environment variables, HTTP errors, and JSON parsing issues.
    """
    # Load required credentials from environment variables
    refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
    client_id = os.getenv("ZOHO_CLIENT_ID")
    client_secret = os.getenv("ZOHO_CLIENT_SECRET")
    redirect_uri = os.getenv("ZOHO_REDIRECT_URI")

    # Ensure all required credentials are present
    if not all([refresh_token, client_id, client_secret, redirect_uri]):
        print("Missing one or more required environment variables.")
        return None

    # Zoho token endpoint and required parameters for refresh
    token_url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }

    try:
        # Make a POST request to fetch a new access token
        response = requests.post(token_url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the response JSON
        token_data = response.json()

        # Check if access_token is present in the response
        if "access_token" not in token_data:
            print(f"Access token not found in response: {token_data}")
            return None

        return token_data["access_token"]

    except requests.exceptions.RequestException as e:
        # Handle network or HTTP errors
        print(f"Error requesting access token: {e}")
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error parsing access token response JSON: {e}")

    return None

def fetch_zoho_contacts():
    """
    Fetches all contacts from Zoho CRM.
    Handles access token retrieval, HTTP errors, and invalid API responses.
    """
    # Get a valid access token
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to get access token."}

    # Zoho Contacts API endpoint
    url = "https://www.zohoapis.com/crm/v2/Contacts"

    # Authorization header with Bearer token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        # Send GET request to fetch contacts
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse response JSON
        data = response.json()

        # Ensure the expected "data" field is present
        if "data" not in data:
            print(f"No 'data' field in response: {data}")
            return {"error": "Unexpected API response structure."}

        return data["data"]

    except requests.exceptions.HTTPError as e:
        # Handle HTTP status errors (e.g., 401, 403)
        print(f"HTTP error when fetching contacts: {e} - {response.text}")
    except requests.exceptions.RequestException as e:
        # Handle network errors
        print(f"Request error when fetching contacts: {e}")
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error parsing contacts JSON: {e}")

    return {"error": "Failed to fetch contacts."}
