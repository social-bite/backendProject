import requests
from django.http import JsonResponse


def getRestaurantInfo(restaurant_id, POCKETBASE_URL, ADMIN_TOKEN):
    """
    Fetches restaurant information by restaurant_id from PocketBase.
    :param restaurant_id: The unique identifier for the restaurant.
    :param POCKETBASE_URL: The base URL for the PocketBase API.
    :param ADMIN_TOKEN: The admin or relevant token to access the PocketBase API.
    :return: A list of restaurant information.
    """
    request_url = f"{POCKETBASE_URL}/api/collections/restaurants/records?filter=(id=\'{restaurant_id}\')"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

    response = requests.get(request_url, headers=headers)

    if response.status_code == 200:
        # Assuming the response contains the restaurant information directly
        data = response.json()
        processedData = []
        for item in data['items']:
            processedData.append({
                "restaurant_id": item['id'],
                "restaurant_name": item['name'],
                "restaurant_address": item['address'],
                "restaurant_open_time": item['open_time'],
                "restaurant_close_time": item['close_time'],
                "restaurant_min_price": item['min_price'],
                "restaurant_max_price": item['max_price']
            })
        return processedData
    else:
        # Handle errors or non-OK responses
        return []
