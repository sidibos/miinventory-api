from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r"products", views.ProductViewSet)
router.register(r"users", views.UserViewSet)
router.register(r"customers", views.CustomerViewSet)
#router.register(r"orders", views.OrderViewSet)
router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"locations", views.LocationViewSet)
router.register(r"shipments", views.ShippingViewSet)
router.register(r"quotations", views.QuotationViewSet)
router.register(r"suppliers", views.SupplierViewSet)
#router.register(r'stocks', views.StockViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'sales-orders', views.SalesOrderViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'transfer-orders', views.TransferOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path("products", views.get_products, name="get.products"),
#     path("users", views.get_users, name="get.users"),
#     path("users/<str:email>/", views.edit_user, name="edit.user"),
#     path("users/create", views.add_user, name="create.user"),
#     path("users/update", views.update_user, name="update.user"),
#     path("users/delete", views.delete_user, name="delete.user"),
#     path("customers", views.CustomerList.as_view(), name="customer.list"),
#     path("customers", views.CustomerList.post, name="customer.list"),
#     path("customers/<int:id>", views.CustomerList.as_view(), name="view.customer"),
#     path("warehouses", views.WareahouseList.as_view(), name="warehouse.list"),
#     path("warehouses/<int:id>", views.WareahouseList.as_view(), name="edit.warehouse"),
#     path("locations", views.LocationList.as_view(), name="location.list"),
#     path("shipments", views.ShippingList.as_view(), name="shipment.list"),
#     path("quotations", views.QuotationList.as_view(), name="quotation.list"),
#     path("suppliers", views.SupplierList.as_view(), name="supplier.list"),
#     path("orders", views.OrderList.as_view(), name="order.list"),
#     path("categories", views.CategoryViewSet.as_view({'get':'list'}), name="category.list"),
#     path("categories", views.CategoryViewSet.as_view({'get':'create'}), name="create.category"),
# ]

#urlpatterns = format_suffix_patterns(urlpatterns)
