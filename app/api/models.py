import uuid
from django.db import models


class User(models.Model):
    """
    User model for the API. This model is stored in the database.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=250, blank=False, null=False)
    email = models.EmailField(max_length=250, unique=True, blank=False, null=False)
    age = models.IntegerField(null=False, blank=False)

    class Meta:
        app_label = "api"

class UserProfile(models.Model):
    """
    UserProfile model, for User model
    """   

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    firtsname = models.CharField(max_length=250, unique=False, blank=True, null=True)
    lastname = models.CharField(max_length=250, unique=False, blank=True, null=True)
    phone = models.CharField(max_length=250, unique=False, blank=True, null=True)
    photo = models.FileField(max_length=250, unique=False, blank=True, null=True)

    class Meta:
        app_label = "api"


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.IntegerField(null=False, blank=False)
    buying_price = models.IntegerField(null=False, blank=False)
    selling_price = models.IntegerField(null=False, blank=False)
    min_stock = models.IntegerField(null=False, blank=False)
    tax = models.IntegerField(null=True, blank=False)
    tax_type = models.IntegerField(null=True, blank=False)
    notes = models.TextField(null=True, blank=False)
    product_image = models.CharField(max_length=255, blank=False, null=True)

    class Meta:
        app_label = "api"
        unique_together = ['user']

