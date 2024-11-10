from django.urls import path
from . import api_views

urlpatterns = [
    path("users", api_views.get_users, name="get_users"),
    path("products", api_views.get_products, name="get_products"),
    path("users/add", api_views.add_user, name="add_user"),
    path("users/update", api_views.update_user, name="update_user"),
    path("users/delete", api_views.delete_user, name="delete_user"),
]
