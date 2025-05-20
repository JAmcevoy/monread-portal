import os
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .utils import fetch_zoho_contacts, get_access_token
from .forms import CustomUserCreationForm


@csrf_exempt
def contact_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            email = user.email
            access_token = get_access_token()
            if not access_token:
                return JsonResponse({"error": "Access token could not be refreshed."}, status=500)

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

def contact_logout(request):
    logout(request)
    return redirect('login')

@staff_member_required
def show_contacts(request):
    contacts = fetch_zoho_contacts()

    if "error" in contacts:
        return JsonResponse({"error": contacts["error"]}, status=400)

    return render(request, 'contacts.html', {'contacts': contacts})


def contact_detail(request, contact_id):
    """
    View for displaying a Zoho CRM contact and its image via secure proxy.
    """
    access_token = get_access_token()
    if not access_token:
        return JsonResponse({'error': 'Failed to get Zoho access token.'}, status=500)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Fetch contact details
    contact_url = f"https://www.zohoapis.com/crm/v2/Contacts/{contact_id}"
    try:
        response = requests.get(contact_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        contact = data['data'][0] if data.get('data') else {}
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch contact details.', 'details': str(e)}, status=500)

    # Fetch account info
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

    # Add image proxy URL to context
    contact['image_url'] = f"/contacts/{contact_id}/photo/"

    return render(request, 'contact_detail.html', {
        'contact': contact,
        'account': account
    })


# 🆕 New view: Proxies Zoho contact photo through your server
def contact_photo(request, contact_id):
    """
    Proxies the contact image from Zoho CRM to avoid authentication issues in <img> tags.
    """
    access_token = get_access_token()
    if not access_token:
        return HttpResponse(status=401)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    photo_url = f"https://www.zohoapis.com/crm/v2/Contacts/{contact_id}/photo"
    try:
        response = requests.get(photo_url, headers=headers, stream=True)
        if response.status_code == 200:
            return HttpResponse(response.content, content_type=response.headers.get('Content-Type', 'image/jpeg'))
        elif response.status_code == 204:
            return HttpResponse(status=204)  # No content (no photo)
        else:
            return HttpResponse(f"Failed to fetch image: {response.status_code}", status=response.status_code)
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error fetching image: {str(e)}", status=500)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # or your main dashboard view
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})