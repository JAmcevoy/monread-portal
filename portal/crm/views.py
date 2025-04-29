# views.py
import os
import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import render
from .utils import fetch_zoho_contacts


@csrf_exempt  # for simplicity; in production, use CSRF protection properly
def contact_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        access_token = os.environ.get("ZOHO_ACCESS_TOKEN")
        if not access_token:
            return JsonResponse({"error": "Access token missing."}, status=500)

        url = "https://www.zohoapis.com/crm/v2/Contacts/search"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        params = {
            "email": email
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('data'):
                contact = data['data'][0]
                return redirect('contact_detail', contact_id=contact['id'])
            else:
                return render(request, "crm/login.html", {"error": "Email not found."})
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Search failed", "details": str(e)}, status=500)

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


def contact_detail(request, contact_id):
    
    access_token = os.environ.get("ZOHO_ACCESS_TOKEN")
    if not access_token:
        return JsonResponse({'error': 'Failed to get Zoho access token.'}, status=500)

    url = f"https://www.zohoapis.com/crm/v2/Contacts/{contact_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        contact = data['data'][0] if data.get('data') else {}
        return render(request, 'contact_detail.html', {'contact': contact})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch contact details.', 'details': str(e)}, status=500)
