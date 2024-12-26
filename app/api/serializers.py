from rest_framework import serializers
from .models import User
from .models import Product
from .models import UserProfile
from .models import Customer
from .models import CustomerUser


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
    users = serializers.SerializerMethodField()
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
            'users'
        ]

    def get_users(self,obj:User):
        users = obj.customeruser_set.all()
        return CustomerUserSerialiser(users,many=True).data      


