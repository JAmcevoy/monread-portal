import os
import requests


def refresh_zoho_access_token(refresh_token=None):
    """
    Refresh the Zoho OAuth access token using the refresh token.
    """
    accounts_url = "https://accounts.zoho.com/oauth/v2/token"

    refresh_token = refresh_token or os.environ.get("ZOHO_REFRESH_TOKEN")
    if not refresh_token:
        print("Missing refresh token.")
        return None, None

    payload = {
        "client_id": os.environ.get("ZOHO_CLIENT_ID"),
        "client_secret": os.environ.get("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(accounts_url, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        access_token = data.get("access_token")
        new_refresh_token = data.get("refresh_token") or refresh_token  # Sometimes refresh_token doesn't change

        if access_token:
            print("Access token refreshed successfully.")
            # Optionally update environment or cache here
            return access_token, new_refresh_token
        else:
            print("No access token returned.")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error refreshing token: {e}")
        return None, None


def fetch_zoho_contacts():
    """
    Fetch contacts from Zoho CRM using the access token.
    Automatically refreshes token on 401 errors.
    """
    access_token = os.environ.get('ZOHO_ACCESS_TOKEN')
    if not access_token:
        print("Access token is missing.")
        access_token, _ = refresh_zoho_access_token()
        if not access_token:
            return {"error": "Access token could not be refreshed."}

    url = f"{os.environ.get('ZOHO_API_DOMAIN', 'https://www.zohoapis.com')}/crm/v2/Contacts?page=1&per_page=200"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 401:
            # Try refreshing and reattempting once
            print("Access token expired. Attempting to refresh.")
            new_token, _ = refresh_zoho_access_token()
            if new_token:
                os.environ['ZOHO_ACCESS_TOKEN'] = new_token
                return fetch_zoho_contacts()
            else:
                return {"error": "Failed to refresh access token."}

        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching contacts: {e}")
        return {"error": "Failed to fetch contacts due to network or API error."}
