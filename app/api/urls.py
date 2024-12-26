from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("products", views.get_products, name="get.products"),
    path("users", views.get_users, name="get.users"),
    path("users/<str:email>/", views.edit_user, name="edit.user"),
    path("users/add", views.add_user, name="add.user"),
    path("users/update", views.update_user, name="update.user"),
    path("users/delete", views.delete_user, name="delete.user"),
    path("customers/", views.CustomerList.as_view(), name="customer.list"),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
