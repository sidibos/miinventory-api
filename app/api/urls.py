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
    path("customers/<int:id>", views.CustomerList.as_view(), name="view.customer"),
    path("warehouses/", views.WareahouseList.as_view(), name="warehouse.list"),
    path("locations/", views.LocationList.as_view(), name="location.list"),
    path("shipments/", views.ShippingList.as_view(), name="shipment.list"),
    path("quotations/", views.QuotationList.as_view(), name="quotation.list"),
    path("suppliers/", views.SupplierList.as_view(), name="supplier.list"),
    # path("orders/", views.OrderList.as_view(), name="order.list"),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
