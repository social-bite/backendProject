import requests
import os
import json
from utils import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Post


POCKETBASE_URL = os.getenv("POCKETBASE_URL")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


@api_view(["POST"])
def create_post(request):
    if not verify(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    data = {
        "user_id": "RELATION_RECORD_ID",
        "restaurant_id": "RELATION_RECORD_ID",
        "menu_item_id": "RELATION_RECORD_ID",
        "restaurant_name": "test",
        "description": "test",
        "price": 123,
        "menu_item_name": "test",
    }

    create_post_helper(request, data)

@api_view(["DELETE"])
def delete_post(request, post_id):
    if not verify(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)
99
    delete_post_helper(post_id)


@api_view(["GET"])
def feed(request):
    if not verify(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    all_posts = getallposts()
    followers = getfollwers()

    if len(all_posts) or len(followers) == 0:
        return JsonResponse({
            "status": 404,
            "data": {"error": "not found"}
        }, status=404)

    # Success
    posts = []
    follow = set()

    for follower in followers['items']:
        follow.add(follower["follower_id"])


    for post in all_posts['items']:
        if post["user_id"] not in follow:
            continue

        record = {
            "id": post.get("record_id", ""),
            "collectionId": post[
                "collectionId", ""
            ],  # Assuming static or from another source
            "collectionName": post[
                "collectionName", ""
            ],  # Assuming static or from another source
            "created": post.get("created", ""),  # Assuming static or from another source
            "updated": post.get("updated", ""),  # Assuming static or from another source
            "user_id": post.get("user_id", ""),
            "user_name": post.get("user_name", ""),
            "image": post.get("image", ""),
            "restaurant_id": post.get("restaurant_id", ""),
            "menu_item_id": post.get("menu_item_id", ""),
            "restaurant_name": post.get("restaurant_name", ""),
            "description": post.get("description", ""),
            "price": post.get("price", 0),
            "menu_item_name": post.get("menu_item_name", ""),
        }

        posts.append(record)

    return JsonResponse({
        "status": 200,
        "posts": posts,
        "message": "Posts data retrieved successfully"
    }, status=200)
