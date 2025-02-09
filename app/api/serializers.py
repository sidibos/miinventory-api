from rest_framework import serializers
from .models import User
from .models import Product
from .models import UserProfile
from .models import Customer, CustomerUser
from .models import Order, OrderDetail
from .models import Supplier, Quotation
from .models import Shipment
from .models import Warehouse, WarehouseProduct
from .models import Location


class UserSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)
    profile = serializers.StringRelatedField(many=False)

    class Meta:
        model = User
        fields = [
            "id",
            "name", 
            "email", 
            "age", 
            "products", 
            "profile", 
            "customers"
        ]
        read_only_fields = [
            "id", 
            "created_at", 
            "updated_at"
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "firstname",
            "lastname",
            "phone",
            "photo"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name", 
            "slug", 
            "code", 
            "quantity", 
            "buying_price", 
            "selling_price",
            "min_stock",
            "tax",
            "tax_type",
            "notes",
            "product_image",
            "warehouses",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class CustomerUserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'customer', 'user']

class CustomerSerialiser(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    sale_orders = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Order.objects.all(), required=False
    )
    class Meta:
        model = Customer
        fields = [
            'id',
            'uuid',
            'name',
            'phone',
            'address',
            'bank_name',
            'account_holder',
            'account_number',
            'short_code',
            'users',
            'sale_orders'
        ]

    def get_users(self, obj:User):
        users = obj.customeruser_set.all()
        return CustomerUserSerialiser(users, many=True).data      

class OrderSerialiser(serializers.ModelSerializer):
    # orderItems = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=OrderDetail.objects.all()
    # )
    class Meta:
        model = Order
        fields = [
            'id',
            'uuid',
            'order_status',
            'sub_total',
            'vat',
            'total_amount',
            'total_items',
            'invoice_no',
            'payment_type',
            'pay',
            'due'
        ]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            's_name',
            'phone',
            'address',
            'email',
            #'website',
            #'notes'
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'order',
            'shipment_date',
            "warehouse",
            "order",
            # 'shipment_status',
            # 'shipment_notes',
            # 'shipment_image'
        ]
        read_only_fields = [
            "id", 
            "created_at", 
            "updated_at"
        ]

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = [
            'customer',
            'date',
            'status',
            "reference",
            'note',
        ]
        read_only_fields = [
            "id", 
            "created_at", 
            "updated_at"
        ]

class WarehouseSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = Warehouse
        fields = [
            'name',
            'capacity',
            'email',
           'products',
        ]
        read_only_fields = [
            "id",
            "created_at", 
            "updated_at"
        ]

class WarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = [
            'id',
            'warehouse',
            'product'
        ]
        read_only_fields = [
            "id"
        ]

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'name',
            # 'phone',
            # 'address',
            # 'notes'
        ]
        read_only_fields = ["id", "name", "created_at", "updated_at"] 
           
