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
    USER_ROLES = [
        ('admin', 'Admin User'),
        ('staff', 'Staff User'),
        ('super_admin', 'Super Admin'),
        ('customer', 'Customer User'),
    ]
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    username = models.CharField(max_length=250, blank=False, null=True)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='customer')
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    #customer = models.ManyToManyField('Customer', through='CustomerUser')
    name = models.CharField(max_length=250, blank=False, null=False)
    email = models.EmailField(max_length=250, unique=True, blank=False, null=False)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        role_display = [role[1] for role in self.USER_ROLES if role[0] == self.role][0]
        return f"{self.username} - {role_display}"

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

    def __str__(self):
        return self.name

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
    name = models.CharField(max_length=250, blank=False, null=False, default='')
    company_name = models.CharField(max_length=250, blank=False, null=False, default='')
    email = models.EmailField(max_length = 254)
    phone = models.CharField(max_length=250, unique=False, blank=True, null=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    class SupplierType(models.TextChoices):
        MANUFACTURER = 'manufacturer'
        DISTRIBUTOR = 'distributor'
        WHOLESALER = 'wholesaler'
        RETAILER = 'retailer'
    supplier_type = models.CharField(choices=SupplierType.choices)
    photo = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    account_holder = models.CharField(max_length=255, null=True)
    account_number = models.CharField(max_length=255, null=True)
    short_code = models.CharField(max_length=255, null=True) 
    bank_name = models.CharField(max_length=255, null=True) 

    def __str__(self):
        return f"Supplier {self.name}"  

class Product(models.Model):
    PRODUCT_STATUS = [
        ('active', 'Active'),
        ('pending', 'Pending'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_by = models.ForeignKey(
        User,  
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products'
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=PRODUCT_STATUS, default='pending')
    sku = models.CharField(max_length=255, blank=False, null=False, unique=True, default='xxx')
    stock = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False, default=0)
    selling_price = models.IntegerField(null=False, blank=False, default=0)
    min_stock = models.IntegerField(null=False, blank=False, default=0)
    tax = models.IntegerField(null=True, blank=False)
    tax_type = models.IntegerField(null=True, blank=False)
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.DO_NOTHING,
        null=True
    )
    product_image = models.ImageField(upload_to ='uploads/', default='uploads/default.jpg', blank=True, null=True)
    supplier = models.ForeignKey(
        Supplier, 
        related_name='products', 
        on_delete=models.DO_NOTHING,
        null=False
    )
    warehouses = models.ManyToManyField('Warehouse', through='WarehouseProduct', null=True)

    # class Meta:
    #     unique_together = ['created_by']

    def __str__(self):
        return self.name        

class Customer(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=250, blank=False, null=False)
    contact_email = models.EmailField(unique=True, null=True, blank=False)
    users = models.ManyToManyField(User, through='CustomerUser', null=True)
    #sale_orders = models.ManyToManyField('Order', through='Order', null=True)
    #contact_person = models.CharField(max_length=250, blank=False, null=False)
    phone = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=255, null=True)
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
    produtcs = models.ManyToManyField(Product, through='WarehouseProduct')
    name = models.CharField(max_length=255, null=False, blank=False)
    capacity = models.IntegerField(null=False, blank=False, default=0)
    email = models.EmailField(max_length = 254)

    def __str__(self):   
        return f"Warehouse {self.name}"
    
class Order(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    customer_user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        null=True
    )
    customer = models.ForeignKey(
        Customer, 
        related_name='sale_orders',
        on_delete=models.DO_NOTHING,
        null=True
    )
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now_add=False)
    class OrderStatus(models.TextChoices):
        PENDING = 'pending'
        FULFILLED = 'fulfilled'
        CANCELLED = 'cancelled'
    order_status = models.CharField(choices=OrderStatus.choices)
    class OrderType(models.TextChoices):
        SALE_ORDER = 'sale order'
        PURCHASE_ORDER = 'purchase'
        TRANSFER_ORDER = 'transfer order'
    order_type = models.CharField(choices=OrderType.choices)
    total_items = models.IntegerField(null=False, blank=False)
    sub_total = models.IntegerField(null=False, blank=False)
    vat = models.IntegerField(null=False, blank=False)
    total_amount = models.IntegerField(null=False, blank=False)
    invoice_no = models.CharField(max_length=255, null=True)
    payment_type = models.CharField(max_length=255, null=True)
    pay = models.IntegerField(null=False, blank=False)
    due = models.IntegerField(null=False, blank=False)
    from_warehouse = models.ForeignKey(
        Warehouse, 
        related_name='outgoing_transfers', 
        on_delete=models.CASCADE,
        null=True
    )
    to_warehouse = models.ForeignKey(
        Warehouse, 
        related_name='incoming_transfers', 
        on_delete=models.CASCADE,
        null=True
    )
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"Order {self.uuid}"

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
    quantity = models.IntegerField(null=False, blank=False, default=0)
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

    def __str__(self):
        return f"Quotation {self.uuid}"

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

    def __str__(self):
        return self.name
    
# Stock Model (Tracks stock levels in warehouses)
class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='stocks', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='stocks', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}"

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

# Shipment Model (Tracks shipments from suppliers to warehouses and warehouses to customers)
class Shipment(models.Model):
    SHIPMENT_TYPES = [
        ('incoming', 'Incoming (Supplier → Warehouse)'),
        ('outgoing', 'Outgoing (Warehouse → Customer)'),
    ]

    shipment_type = models.CharField(max_length=10, choices=SHIPMENT_TYPES, default='incoming')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    shipped_from = models.CharField(max_length=255, null=True)  # Supplier name or warehouse name
    shipped_to = models.CharField(max_length=255, null=True)  # Warehouse or customer name
    shipment_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(
        Order, 
        related_name='order_shipments',
         on_delete=models.DO_NOTHING, 
         null=True
    )

    def save(self, *args, **kwargs):
        if self.shipment_type == 'incoming':  # Supplier → Warehouse
            stock, created = Stock.objects.get_or_create(product=self.product, warehouse=self.warehouse)
            stock.quantity += self.quantity  # Increase stock
            stock.save()
        elif self.shipment_type == 'outgoing':  # Warehouse → Customer
            stock = Stock.objects.get(product=self.product, warehouse=self.warehouse)
            if stock.quantity >= self.quantity:
                stock.quantity -= self.quantity  # Decrease stock
                stock.save()
            else:
                raise ValueError("Not enough stock available!")
        super().save(*args, **kwargs)              

# class Shipment(TimeStampedModel):
#     shipment_date = models.DateTimeField(auto_now_add=False)
#     #status = 
#     warehouse = models.ForeignKey(
#         Warehouse, 
#         related_name='warehouse_shipments',
#          on_delete=models.DO_NOTHING, 
#          null=True
#     )
#     order = models.ForeignKey(
#         Order, 
#         related_name='order_shipments',
#          on_delete=models.DO_NOTHING, 
#          null=True
#     )

    #photo = models.ImageField(upload_to='images/', blank=True, null=True, null=True)


