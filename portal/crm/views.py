from django.shortcuts import render
from django.http import HttpResponse
import requests
import os

# Function to get Zoho access token
def get_zoho_access_token():
    url = f"{os.environ.get('ZOHO_API_DOMAIN')}/oauth/v2/token"
    params = {
        "refresh_token": os.environ.get("ZOHO_REFRESH_TOKEN"),
        "client_id": os.environ.get("ZOHO_CLIENT_ID"),
        "client_secret": os.environ.get("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token",
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

# Function to fetch customer data from Zoho API based on email
def fetch_zoho_customer(email):
    access_token = get_zoho_access_token()
    url = f"{os.environ.get('ZOHO_API_DOMAIN')}/crm/v2/Leads/search"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    params = {"email": email}  # Search by email
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    if data.get("data"):
        # Assuming only one result for the given email
        return data["data"][0]
    return None

# The view to display customer info
def customer_info(request):
    contact = None
    if 'email' in request.GET:
        email = request.GET.get('email')
        contact_data = fetch_zoho_customer(email)
        if contact_data:
            contact = {
                "name": contact_data.get("Full_Name", "-"),
                "company_name": contact_data.get("Company", "-"),
                "support_time_left": contact_data.get("Support_Time_Left", "-")  # Adjust this based on the Zoho field name
            }

    return render(request, "crm/customer_info.html", {"contact": contact})
