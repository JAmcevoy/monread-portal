# views.py
import os
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .utils import fetch_zoho_contacts, refresh_zoho_access_token


# View to refresh the Zoho access token
def refresh_access_token(request):
    access_token = os.environ.get("ZOHO_ACCESS_TOKEN")
    if access_token:
        return JsonResponse({"message": "Access token is already available."}, status=200)
    
    # If no access token, attempt to refresh it
    new_token = refresh_zoho_access_token()
    if new_token:
        os.environ['ZOHO_ACCESS_TOKEN'] = new_token
        return JsonResponse({"message": "Access token refreshed successfully."}, status=200)
    else:
        return JsonResponse({"error": "Failed to refresh access token."}, status=400)

@csrf_exempt
def contact_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate using username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in

            # Then use their email to search Zoho contact
            email = user.email
            access_token = os.environ.get("ZOHO_ACCESS_TOKEN")
            if not access_token:
                return JsonResponse({"error": "Access token missing."}, status=500)

            url = "https://www.zohoapis.com/crm/v2/Contacts/search"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            params = {
                "criteria": f"(Email:equals:{email})"
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                if data.get('data'):
                    contact = data['data'][0]
                    return redirect('contact_detail', contact_id=contact['id'])
                else:
                    return render(request, "login.html", {"error": "No CRM contact found for this email."})
            except requests.exceptions.RequestException as e:
                return JsonResponse({"error": "Zoho contact search failed", "details": str(e)}, status=500)
        else:
            return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")

# View to display the contacts from Zoho CRM
@staff_member_required
def show_contacts(request):
    contacts = fetch_zoho_contacts()  # Call the function to fetch contacts

    # If an error occurred while fetching contacts, return an error response
    if "error" in contacts:
        return JsonResponse({"error": contacts["error"]}, status=400)

    # If contacts were fetched successfully, return them as JSON
    return render(request, 'contacts.html', {'contacts': contacts})

# View to display the contact details from Zoho CRM
def contact_detail(request, contact_id):
    access_token = os.environ.get("ZOHO_ACCESS_TOKEN")
    if not access_token:
        return JsonResponse({'error': 'Failed to get Zoho access token.'}, status=500)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Step 1: Get the Contact
    contact_url = f"https://www.zohoapis.com/crm/v2/Contacts/{contact_id}"
    try:
        response = requests.get(contact_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        contact = data['data'][0] if data.get('data') else {}
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch contact details.', 'details': str(e)}, status=500)

    # Step 2: Get the associated Account
    account = {}
    account_id = contact.get("Account_Name", {}).get("id")
    if account_id:
        account_url = f"https://www.zohoapis.com/crm/v2/Accounts/{account_id}"
        try:
            acc_response = requests.get(account_url, headers=headers)
            acc_response.raise_for_status()
            acc_data = acc_response.json()
            account = acc_data['data'][0] if acc_data.get('data') else {}
        except requests.exceptions.RequestException as e:
            account = {"error": "Failed to fetch account details", "details": str(e)}

    # Step 3: Render both
    return render(request, 'contact_detail.html', {
        'contact': contact,
        'account': account
    })
    
    
    
