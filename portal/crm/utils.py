# utils.py
import os
import requests

# Function to refresh the Zoho OAuth access token
def refresh_zoho_access_token():
    url = f"{os.environ.get('ZOHO_API_DOMAIN')}/oauth/v2/token"
    params = {
        "refresh_token": os.environ.get("ZOHO_REFRESH_TOKEN"),
        "client_id": os.environ.get("ZOHO_CLIENT_ID"),
        "client_secret": os.environ.get("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token",
    }

    try:
        response = requests.post(url, data=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "access_token" in data:
            return data["access_token"]
        else:
            return None

    except requests.exceptions.RequestException:
        return None

# Function to fetch contacts from Zoho CRM
def fetch_zoho_contacts():
    access_token = os.environ.get('ZOHO_ACCESS_TOKEN')  
    if not access_token:
        return {"error": "Access token is missing. Please refresh the token."}

    url = f"{os.environ.get('ZOHO_API_DOMAIN')}/crm/v2/Contacts?page=1&per_page=200"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "data" in data:
            return data["data"]
        else:
            return {"error": "Failed to fetch contacts."}

    except requests.exceptions.RequestException as e:
        if response.status_code == 401:
            new_access_token = refresh_zoho_access_token()
            if new_access_token:
                os.environ['ZOHO_ACCESS_TOKEN'] = new_access_token
                return fetch_zoho_contacts()
            else:
                return {"error": "Failed to refresh access token."}
        else:
            return {"error": "Failed to fetch contacts."}
