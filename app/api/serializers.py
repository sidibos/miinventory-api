from rest_framework import serializers
from .models import User
from .models import Product
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)
    profile = serializers.StringRelatedField(many=False)

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

