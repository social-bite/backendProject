from django.urls import path
from .views import *

urlpatterns = [
    path('restaurants/', getRestaurants, name='getRestaurants'),
    path('restaurant/<str:restaurant_id>/menu', getRestaurantMenu, name='getRestaurantMenu'),
]
