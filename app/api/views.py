import re
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import User, Customer, CustomerUser, Shipment, Supplier
from .serializers import UserSerializer, CustomerSerialiser, CustomerUserSerialiser
from .models import Product, Warehouse, Order, Location, Quotation, Category
from .serializers import ProductSerializer
from .serializers import WarehouseSerializer
from .serializers import LocationSerializer, OrderSerialiser, ShipmentSerializer, SupplierSerializer
from .serializers import QuotationSerializer, CategorySerializer
from django.shortcuts import get_object_or_404


# The swagger_auto_schema decorator is used to document the API endpoints.
@swagger_auto_schema(
    method="get",
    operation_summary="Lists all products",
    operation_description="API endpoint that retrieves all products and returns them in JSON "
    "format.",
    responses={
        200: "All products in JSON format",
        400: "Bad request: Check error message for details",
        500: "Internal server error: Unexpected error",
    },
)
@api_view(["GET"])
def get_products(request):
    """
    API endpoint that retrieves all products.

    For retrieving all products, send a GET request without any parameters.

    :return: A JSON response with a list of all users or the requested user data.
             Returns an error response if the "email" parameter is missing or the
             requested user is not found.
    """

    # Return all products
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        return Response(serializer.data)

    # Catch unexpected errors and return a 500 response
    except Exception as e:
        return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@swagger_auto_schema(
    method="get",
    operation_summary="Lists all users or a single user by email",
    operation_description="API endpoint that retrieves all users or a single user by email and returns them in JSON "
    "format.",
    manual_parameters=[
        openapi.Parameter(
            "email",
            openapi.IN_QUERY,
            description="User is searched by this email and returned if found. Optional, if not "
            "present, all users are returned.",
            type=openapi.TYPE_STRING,
        )
    ],
    responses={
        200: "One or all users in JSON format",
        400: "Bad request: Check error message for details",
        404: "If user was requested by email but not found",
        500: "Internal server error: Unexpected error",
    },
)
@api_view(["GET"])
def get_users(request):
    """
    API endpoint that retrieves all users or a single user by email.

    For retrieving all users, send a GET request without any parameters.

    For retrieving a single user, send a GET request with an "email" parameter
    that specifies the email address of the user to retrieve.

    :param request: A GET request object.
    :return: A JSON response with a list of all users or the requested user data.
             Returns an error response if the "email" parameter is missing or the
             requested user is not found.
    """

    # Return a single user if email parameter is provided
    if "email" in request.GET:
        email = request.GET["email"]

        # Check for empty email parameter
        if not email:
            return Response(
                {"result": "error", "message": "Email parameter is missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Return requested user
        try:
            user = get_object_or_404(User, email=email)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        # Catch Http404 raised by get_object_or_404() if user is not found
        except Http404:
            return Response({"result": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Return all users
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # Catch unexpected errors and return a 500 response
    except Exception as e:
        return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def edit_user(request, email=''):
    # Return requested user
    try:
        #validateEmail = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not valid_email:
            raise ValidationError("Invalid Email")
    
        user = get_object_or_404(User, email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # Catch Http404 raised by get_object_or_404() if user is not found
    except Http404:
        return Response({"result": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({"result": "error", "message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method="post",
    operation_summary="Creates new user",
    operation_description="API endpoint that creates a new user and returns the created user in JSON format.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the user"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email of the user"),
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username of the user"),
            "age": openapi.Schema(type=openapi.TYPE_INTEGER, description="Age of the user"),
        },
        required=["name", "email", "age"],
    ),
    responses={
        201: "Return the created user in JSON format",
        400: "Bad request: Check error message for details",
        500: "Internal server error: Unexpected error",
    },
)
@api_view(["POST"])
def add_user(request):
    """
    API endpoint that creates a new user and returns the created user in JSON format.

    :param request: POST request with name, email and age in JSON format
    :return: JSON response with newly created user or error message
    """

    # Try to create a new user
    try:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"result": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)

    # Catch validation errors and return a 400 response
    except ValidationError as e:
        return Response({"result": "error", "message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    # Catch unexpected errors and return a 500 response
    except Exception as e:
        return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="put",
    operation_summary="Updates existing user",
    operation_description="API endpoint that updates an existing users name and age by provided email and returns "
    "updated user in JSON format.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="Update the name of the user"),
            "age": openapi.Schema(type=openapi.TYPE_INTEGER, description="Update the age of the user"),
        },
        required=["name", "age"],
    ),
    manual_parameters=[
        openapi.Parameter(
            "email", openapi.IN_QUERY, description="Email of the user to update", type=openapi.TYPE_STRING
        )
    ],
    responses={
        200: "Return the created user in JSON format",
        400: "Bad request: Check error message for details",
        404: "No user found with the provided email address",
        500: "Internal server error: Unexpected error",
    },
)
@api_view(["PUT"])
def update_user(request):
    """
    API endpoint that updates an existing users name and age by provided email.

    :param request: PUT request with user data and email parameter
    :return: JSON response with user data or error message
    """

    email = request.query_params.get("email")

    # Check for empty email parameter
    if not email:
        return Response(
            {"result": "error", "message": "Email parameter is missing"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Try to get the user by email
    try:
        user = get_object_or_404(User, email=email)
        # Ensure that the email address won"t be changed
        request_data = request.data.copy()
        request_data["email"] = email

    # Catch Http404 raised by get_object_or_404() if user is not found
    except Http404:
        return Response({"result": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Catch unexpected errors and return a 500 response
    except Exception as e:
        return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Try to update the user
    try:
        serializer = UserSerializer(user, data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"result": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    # Catch validation errors and return a 400 response
    except ValidationError as e:
        return Response({"result": "error", "message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    # Catch unexpected errors and return a 500 response
    except Exception as e:
        return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="delete",
    operation_summary="Deletes existing user",
    operation_description="API endpoint that deletes an existing user record by email",
    manual_parameters=[
        openapi.Parameter(
            "email", openapi.IN_QUERY, description="Email of the user to be deleted", type=openapi.TYPE_STRING
        )
    ],
    responses={
        204: "Success: User deleted",
        400: "Bad request: Check error message for details",
        404: "No user found with the provided email address",
        500: "Internal server error: Unexpected error",
    },
)
@api_view(["DELETE"])
def delete_user(request):
    """
    API endpoint that deletes an existing user record by email.

    :param request: DELETE request with email parameter as a query parameter in the URL
    :return: JSON response with success or error message
    """

    email = request.query_params.get("email")

    # Check for empty email parameter
    if not email:
        return Response(
            {"result": "error", "message": "Email parameter is missing"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Delete user
    try:
        user = get_object_or_404(User, email=email)
        user.delete()
        return Response({"result": "success", "message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

    # Catch Http404 raised by get_object_or_404() if user is not found
    except Http404:
        return Response({"result": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Catch unexpected errors and return a 500 response
    except Exception as e:
        return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(
            {
                "result": "success", 
                "data": serializer.data,
                "total": len(serializer.data)
            }, 
            status=status.HTTP_201_CREATED
        )

class CustomerViewSet(viewsets.ModelViewSet): 
    queryset = Customer.objects.all()
    serializer_class = CustomerSerialiser    

class OrderViewSet(viewsets.ModelViewSet):  
    queryset = Order.objects.all()
    serializer_class = OrderSerialiser


class WarehouseViewSet(viewsets.ModelViewSet):  
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class LocationViewSet(viewsets.ModelViewSet):  
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ShippingViewSet(viewsets.ModelViewSet):  
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class QuotationViewSet(viewsets.ModelViewSet):  
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

# class StockViewSet(viewsets.ModelViewSet):    
#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer

class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerialiser

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()

            if request.data.get("user"):
                customer_user_data = {
                    "customer": serializer.data.get("id"),
                    "user": request.data.get("user")
                }
                customerUserSerializer = CustomerUserSerialiser(data=customer_user_data)
                customerUserSerializer.is_valid(raise_exception=True)
                customerUserSerializer.save()
        except Exception as e:
            return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"result": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)

class WareahouseList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerialiser

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(order_type='purchase_order')
    serializer_class = OrderSerialiser

    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerialiser(orders, many=True)
        return Response(
            {
                "result": "success", 
                "data": serializer.data,
                "total": len(serializer.data)
            }, 
            status=status.HTTP_201_CREATED
        )

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(order_type='sale_order')
    serializer_class = OrderSerialiser 

    def list(self, request):
        orders = Order.objects.all()
        serializer = ProductSerializer(orders, many=True)
        return Response(
            {
                "result": "success", 
                "data": serializer.data,
                "total": len(serializer.data)
            }, 
            status=status.HTTP_201_CREATED
        )

class TransferOrderViewSet(viewsets.ModelViewSet):   
    queryset = Order.objects.filter(order_type='transfer_order')
    serializer_class = OrderSerialiser

class ShippingList(generics.ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class QuotationList(generics.ListAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer    

class SupplierList(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

# class StockViewSet(viewsets.ModelViewSet):
#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        supplier_id = self.kwargs.get('id')
        products = Product.objects.filter(supplier=supplier_id)
        serializer = ProductSerializer(products, many=True)
        return Response(
            {
                "result": "success", 
                "data": serializer.data,
                "total": len(serializer.data)
            }, 
            status=status.HTTP_200_OK
        )

    # def get_products(self, request, *args, **kwargs):
    #     print(self.kwargs)
    #     exit()
    #     supplier_id = self.kwargs.get('id')
    #     products = Product.objects.filter(supplier=supplier_id)
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(
    #         {
    #             "result": "success", 
    #             "data": serializer.data,
    #             "total": len(serializer.data)
    #         }, 
    #         status=status.HTTP_201_CREATED
    #     )

    # def get_queryset(self):
    #     supplier_id = self.kwargs.get('id')
    #     return Product.objects.filter(supplier=supplier_id)