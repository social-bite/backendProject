import requests
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .utils import getRestaurantInfo

POCKETBASE_URL = os.getenv('POCKETBASE_URL')
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')


@require_http_methods(['GET'])
@csrf_exempt
def getRestaurants(request):
    """
    Get a list of restaurants
    :param request:
    :return: JsonResponse
    """

    # Construct the request URL and headers
    requestURL = f'{POCKETBASE_URL}/api/collections/restaurants/records?perPage=15&sort=id'
    headers = {
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }

    # Send GET request to PocketBase to retrieve restaurants list
    response = requests.get(requestURL, headers=headers)

    # Check the response status and return the JSON response accordingly
    if response.status_code == 200:
        # Success
        data = response.json()
        processedRestaurantData = []
        for restaurant in data['items']:
            processedRestaurantData.append({
                "id": restaurant['id'],
                "name": restaurant['name'],
                "address": restaurant['address'],
                "open_time": restaurant['open_time'],
                "close_time": restaurant['close_time'],
                "min_price": restaurant['min_price'],
                "max_price": restaurant['max_price']
            })
        return JsonResponse({
            "status": response.status_code,
            "restaurantData": processedRestaurantData,
            "message": "Restaurants data retrieved successfully"
        }, status=200)
    else:
        # Error
        return JsonResponse({
            "status": response.status_code,
            "data": {"error": response.text}
        }, status=response.status_code)


@require_http_methods(['GET'])
@csrf_exempt
def getRestaurantMenu(request, restaurant_id):
    """
    Get the menu of a restaurant
    :param request:
    :param restaurant_id:
    :return: JsonResponse
    """

    # Construct the request URL and headers
    requestURL = f'{POCKETBASE_URL}/api/collections/menu_items/records?page=1&perPage=50&sort=id&filter=(restaurant_id=\'{restaurant_id}\')'
    headers = {
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }

    # Send GET request to PocketBase to retrieve restaurant menu
    response = requests.get(requestURL, headers=headers)

    # Check the response status and return the JSON response accordingly
    if response.status_code == 200:
        data = response.json()
        processMenuItemData = []
        # get restaurant info
        processRestaurantData = getRestaurantInfo(restaurant_id, POCKETBASE_URL, ADMIN_TOKEN)[0]

        for itemDict in data['items']:
            processedMenuItem = {
                "id": itemDict['id'],
                "name": itemDict['name'],
                "price": itemDict['price'],
                "description": itemDict['description'],
                "created": itemDict['created'],
                "updated": itemDict['updated']
            }
            processMenuItemData.append(processedMenuItem)
        return JsonResponse({
            "status": response.status_code,
            "restaurantData": processRestaurantData,
            "menuData": processMenuItemData,
            "message": "Restaurant menu data retrieved successfully"
        }, status=200)
    else:
        # Error
        return JsonResponse({
            "status": response.status_code,
            "data": {"error": response.text}
        }, status=response.status_code)
