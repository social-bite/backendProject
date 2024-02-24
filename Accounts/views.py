import requests
import json
import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .utils import *

POCKETBASE_URL = os.getenv('POCKETBASE_URL')


@require_http_methods(['POST'])
@csrf_exempt
def register(request):
    """
    Register a new user
    :param request:
    :return: JsonResponse
    """

    requestURL = f'{POCKETBASE_URL}/api/collections/users/records'
    # Deserialize JSON data from request.body
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    requestURL = f'{POCKETBASE_URL}/api/collections/users/records'
    userData = {
        'username': data.get('username'),  # Use .get to avoid KeyError
        'password': data.get('password'),
        'passwordConfirm': data.get('passwordConfirm'),
        # Add more fields as needed
    }
    response = requests.post(requestURL, json=userData)
    response_dict = {"status": response.status_code}
    if (response.status_code == 200):
        response_dict["data"] = response.json()
    else:
        response_dict["error"] = response.text
    return JsonResponse(response_dict, status=response.status_code)
    # return JsonResponse({
    #     "status": response.status_code,
    #     "data": response.json() if response.status_code == 200 else {"error": response.text}
    # }, status=response.status_code)


@require_http_methods(['POST'])
@csrf_exempt
def login(request):
    """
    Log in a user
    :param request:
    :return: JSONResponse
    """

    requestURL = f'{POCKETBASE_URL}/api/collections/users/auth-with-password'
    # Deserialize JSON data from request.body
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    credentials = {
        "identity": data.get('username'),
        "password": data.get('password')
    }

    response = requests.post(requestURL, json=credentials)
    if response.status_code == 200:
        # extract the user ID from the response
        user_id = response.json().get('record', {}).get('id')
        token = response.json().get('token')
        if user_id:
            # store the user ID in the session
            request.session['pb_user_id'] = user_id
            request.session['pb_auth_token'] = token

            responseData = {
                "status": response.status_code,
                "data": response.json(),
                "message": "Login successful"
            }
        else:
            responseData = {
                "status": 400,
                "message": "Invalid response from server"
            }
    else:
        responseData = {
            "status": response.status_code,
            "message": "Invalid credentials",
            # "data": {"error": "Invalid credentials"},
        }
    return JsonResponse(responseData, status=response.status_code)


@require_http_methods(['POST'])
@csrf_exempt
def logout(request):
    """
    Log out a user
    :param request:
    :return: JSONResponse
    """

    # Clear the PB auth token and user ID from the session
    request.session.pop('pb_user_id', None)
    request.session.pop('pb_auth_token', None)
    return JsonResponse({"status": 200, "message": "Logout successful"}, status=200)


@require_http_methods(['PATCH'])
@csrf_exempt
def updateAccount(request):
    """
    Update user account
    :param request:
    :return: JSONResponse
    """

    # Ensure user is logged in
    pb_auth_token = request.session.get('pb_auth_token')
    if not pb_auth_token:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    # Deserialize JSON data from request.body
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_id = request.session.get('pb_user_id')
    requestURL = f'{POCKETBASE_URL}/api/collections/users/records/{user_id}'
    headers = {
        "Authorization": f"Bearer {pb_auth_token}",
        "Content-Type": "application/json"
    }

    updatedData = prepareUpdatedData(data, user_id)
    print("updatedData = ", updatedData)

    response = requests.patch(requestURL, json=updatedData, headers=headers)
    if response.status_code == 200:
        return JsonResponse({
            "data": response.json(),
            "message": "Account updated successfully"
        }, status=200)
    else:
        return JsonResponse({
            "data": {"error": response.text}
        }, status=response.status_code)
