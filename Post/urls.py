from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("posts/create_post/", views.create_post, name="create_post"),
    path("posts/delete_post/<str:post_id>", views.delete_post, name="delete_post"),
    path("posts/feed/", views.feed, name="feed"),
]
