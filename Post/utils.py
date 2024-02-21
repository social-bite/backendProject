import requests
import os
from django.http import JsonResponse


POCKETBASE_URL = os.getenv("POCKETBASE_URL")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

def getallposts(request):
    requestURL = f"{POCKETBASE_URL}/api/collections/posts/records"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

    response = requests.get(requestURL, headers=headers)
    if response.status_code == 200:
        return response.json()

    return []

def verify(request):
    pb_auth_token = request.session.get("pb_auth_token")
    if not pb_auth_token:
        JsonResponse({"error": "Unauthorized"}, status=401)
        return False

    return True

def getfollwers(request):
    pb_auth_token = request.session.get("pb_auth_token")
    if not pb_auth_token:
        JsonResponse({"error": "Unauthorized"}, status=401)
        return False

    requestURL = f"{POCKETBASE_URL}/api/collections/follows/records"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

    response = requests.get(requestURL, headers=headers)
    if response.status_code == 200:
        return response.json()
    
    return []

def create_post_helper(request, data):
    requestURL = f"{POCKETBASE_URL}/api/collections/posts/records"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    response = requests.post(requestURL, headers=headers, json = data)

    

def delete_post_helper(request, id):
    requestURL = f"{POCKETBASE_URL}/api/collections/posts/records/:{id}"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    response = requests.delete(requestURL, headers=headers)
