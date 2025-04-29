# views.py
from django.http import JsonResponse
from django.shortcuts import render
from .utils import fetch_zoho_contacts

# View to display the contacts from Zoho CRM
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
