import uuid
from django.db import models
from datetime import datetime

class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  
        app_label = "api"      

class Country(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=250, blank=False, null=False)
    code = models.CharField(max_length=5, blank=False, null=False)

class Address(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, 
        related_name='addresses', 
        on_delete=models.DO_NOTHING, 
        null=True
    )

class User(TimeStampedModel):
    """
    User model for the API. This model is stored in the database.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=250, blank=False, null=False)
    email = models.EmailField(max_length=250, unique=True, blank=False, null=False)
    age = models.IntegerField(null=True, blank=False)

class UserProfile(TimeStampedModel):
    """
    UserProfile model, for User model
    """   

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    firtsname = models.CharField(max_length=250, unique=False, blank=True, null=True)
    lastname = models.CharField(max_length=250, unique=False, blank=True, null=True)
    phone = models.CharField(max_length=250, unique=False, blank=True, null=True)
    photo = models.FileField(max_length=250, unique=False, blank=True, null=True)

class Category(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False, null=False)   
    slug = models.SlugField(max_length=255)
    created_by = models.ForeignKey(
        User, 
        related_name='categories', 
        on_delete=models.DO_NOTHING, 
        null=True
    )

class Supplier(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    created_by = models.ForeignKey(
        User, 
        related_name='created_suppliers', 
        on_delete=models.DO_NOTHING, 
        null=True
    )
    contact_person = models.OneToOneField(
        User,  
        on_delete=models.DO_NOTHING, 
        null=True
    )
    s_name = models.CharField(max_length=250, blank=False, null=False, default='')
    email = models.EmailField(max_length = 254)
    phone = models.CharField(max_length=250, unique=False, blank=True, null=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    class SupplierType(models.TextChoices):
        PRODUCER = 'producer'
        DISTRIBUTOR = 'distributor'
        WHOLESALER = 'wholesaler'
    supply_type = models.CharField(choices=SupplierType.choices)
    photo = models.ImageField(upload_to ='uploads/')
    account_holder = models.CharField(max_length=255, null=True)
    account_number = models.CharField(max_length=255, null=True)
    short_code = models.CharField(max_length=255, null=True) 
    bank_name = models.CharField(max_length=255, null=True) 

def __str__(self):
        return f"Supplier {self.name}"     

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False)
    sku = models.CharField(max_length=255, blank=False, null=False, unique=True, default='xxx')
    code = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.IntegerField(null=False, blank=False)
    buying_price = models.IntegerField(null=False, blank=False)
    selling_price = models.IntegerField(null=False, blank=False)
    min_stock = models.IntegerField(null=False, blank=False)
    tax = models.IntegerField(null=True, blank=False)
    tax_type = models.IntegerField(null=True, blank=False)
    notes = models.TextField(null=True, blank=False)
    product_image = models.ImageField(upload_to ='uploads/')
    supplier = models.ForeignKey(
        Supplier, 
        related_name='products', 
        on_delete=models.DO_NOTHING,
        null=False,
        default=''
    )

    class Meta:
        unique_together = ['created_by']


class Customer(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=250, blank=False, null=False)
    #contact_person = models.CharField(max_length=250, blank=False, null=False)
    phone = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=255, null=True, blank=False)
    bank_name = models.CharField(max_length=255, null=True)
    account_holder = models.CharField(max_length=255, null=True)
    account_number = models.CharField(max_length=255, null=True)
    short_code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Customer {self.name}" 
    
class CustomerUser(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_person = models.BooleanField(default=False)

class Order(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    customer_user = models.ForeignKey(User, related_name='saleOrders', on_delete=models.DO_NOTHING, null=True)
    customer = models.ForeignKey(
        Customer, 
        related_name='orders',
        on_delete=models.DO_NOTHING
    )
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now_add=False)
    class OrderStatus(models.TextChoices):
        PENDING = 'pending'
        FULFILLED = 'fulfilled'
        CANCELLED = 'cancelled'
    order_status = models.CharField(choices=OrderStatus.choices)
    class OrderType(models.TextChoices):
        SALE = 'sale'
        PURCHASE = 'purchase'
        TRANSFER = 'transfer'
    order_type = models.CharField(choices=OrderType.choices)
    total_items = models.IntegerField(null=False, blank=False)
    sub_total = models.IntegerField(null=False, blank=False)
    vat = models.IntegerField(null=False, blank=False)
    total_amount = models.IntegerField(null=False, blank=False)
    invoice_no = models.CharField(max_length=255, null=True)
    payment_type = models.CharField(max_length=255, null=True)
    pay = models.IntegerField(null=False, blank=False)
    due = models.IntegerField(null=False, blank=False)

class OrderDetail(TimeStampedModel):
    order = models.ForeignKey(
        Order, 
        related_name='orderItems', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False)
    unitcost = models.IntegerField(null=False, blank=False)
    total_amount = models.IntegerField(null=False, blank=False)

    class Meta:
        unique_together = ['order', 'product']

class Quotation(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=255, null=False)
    customer = models.ForeignKey(
        Customer, 
        related_name='quotations', 
        null=True,
        on_delete=models.CASCADE
    )
    tax_percentage = models.IntegerField(null=False, blank=False, default=0)
    tax_amount = models.IntegerField(null=False, blank=False, default=0)
    discount_percentage = models.IntegerField(null=False, blank=False, default=0)
    discount_amount = models.IntegerField(null=False, blank=False, default=0)
    shipping_amount = models.IntegerField(null=False, blank=False, default=0)
    total_amount = models.IntegerField(null=False, blank=False)
    class QuotationStatus(models.TextChoices):
        PENDING = 'pending'
        IN_PROGRESS = 'in_progress'
        APPROVED = 'approved'
        REJECTED = 'rejected'
    status = models.CharField(choices=QuotationStatus.choices)
    note = models.TextField()
    created_by = models.ForeignKey(
        User, 
        related_name='updated_by_user',
         on_delete=models.DO_NOTHING, 
         null=True
    )

class Unit(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.CharField(max_length=255, null=False, blank=False)
    short_code = models.CharField(max_length=255, null=True, blank=False)
    created_by = models.ForeignKey(
        User, 
        related_name='created_by_user',
         on_delete=models.DO_NOTHING, 
         null=True
    ) 

class Location(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)

class Warehouse(TimeStampedModel):
    location = models.ForeignKey(
        Location, 
        related_name='warehouses',
         on_delete=models.DO_NOTHING, 
         null=True
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    capacity = models.IntegerField(null=False, blank=False, default=0)
    email = models.EmailField(max_length = 254)

class WarehouseProduct(TimeStampedModel):
    warehouse = models.ForeignKey(
        Warehouse, 
        related_name='warehouse_products',
         on_delete=models.DO_NOTHING, 
         null=True
    )
    product = models.ForeignKey(
        Product, 
        related_name='product_warehouses',
         on_delete=models.DO_NOTHING, 
         null=True
    )

class Shipment(TimeStampedModel):
    shipment_date = models.DateTimeField(auto_now_add=False)
    #status = 
    warehouse = models.ForeignKey(
        Warehouse, 
        related_name='warehouse_shipments',
         on_delete=models.DO_NOTHING, 
         null=True
    )
    order = models.ForeignKey(
        Order, 
        related_name='order_shipments',
         on_delete=models.DO_NOTHING, 
         null=True
    )

    #photo = models.ImageField(upload_to='images/', blank=True, null=True, null=True)


