from rest_framework import serializers
from .models import User
from .models import Product
from .models import UserProfile
from .models import Customer
from .models import CustomerUser
from .models import Order
from .models import OrderDetail, Supplier, Quotation
from .models import Shipment
from .models import Warehouse
from .models import Location


class UserSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)
    profile = serializers.StringRelatedField(many=False)
    customers = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ["name", "email", "age", "products", "profile"]
        read_only_fields = ["id", "created_at", "updated_at"]

class UserProfile(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(many=False)
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
            "product_image"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class CustomerUserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'customer', 'user']

class CustomerSerialiser(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )
    sale_orders = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Order.objects.all()
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

    def get_users(self,obj:User):
        users = obj.customeruser_set.all()
        return CustomerUserSerialiser(users,many=True).data      

class OrderSerialiser(serializers.ModelSerializer):
    orderItems = serializers.PrimaryKeyRelatedField(
        many=True, queryset=OrderDetail.objects.all()
    )
    class Meta:
        model = Order
        fields = [
            'id',
            'uuid',
            'order_status',
            'total_products',
            'sub_total',
            'vat',
            'total',
            'invoice_no',
            'payment_type',
            'pay',
            'due'
        ]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'phone',
            'address',
            'email',
            'website',
            'notes'
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'order',
            'shipment_date',
            # 'shipment_status',
            # 'shipment_notes',
            # 'shipment_image'
        ]
        read_only_fields = ["id", "shipment_date","created_at", "updated_at"]

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
        read_only_fields = ["id", "customer", "date", "status", "created_at", "updated_at"]

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'name',
            'capacity',
            'email'
        ]
        read_only_fields = ["id", "name", "capacity", "email", "created_at", "updated_at"]

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
           
