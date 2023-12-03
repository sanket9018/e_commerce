from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from . utils import (
    get_response,
    get_status_msg,
    Generate_Order_Number   
)

from . models import (
    Customer,
    Product,
    Order,
    Order_item,
)

from . serializer import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


def home(request):
    return HttpResponse("Hyyyy")

class CustomersAPI(APIView):

    def get_queryset(self):
        all_customers = Customer.objects.all()
        return all_customers

    def get(self, request):

        all_customers = self.get_queryset()
        
        if not all_customers: 
            return get_response(status.HTTP_404_NOT_FOUND, [], get_status_msg('DATA_NOT_FOUND'))

        serializer = CustomerSerializer(all_customers, many = True)
        return get_response(status.HTTP_200_OK, serializer.data, get_status_msg('RETRIEVE'))
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request):

        data = request.data
        serializer = CustomerSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return get_response(status.HTTP_200_OK, serializer.data, get_status_msg("CREATED"))
        
        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400"))

class CustomersUpdateAPI(APIView):

    def get_queryset(self, id):
        customer = Customer.objects.filter(id = id).first()
        return customer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name' : openapi.Schema(type=openapi.TYPE_STRING),
                'contact_number' : openapi.Schema(type=openapi.TYPE_STRING),
                'email' : openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def put(self, request, id):

        customer = self.get_queryset(id)
        if not customer:
            return get_response(status.HTTP_404_NOT_FOUND, {}, get_status_msg('DATA_NOT_FOUND'))

        data = request.data

        serializer = CustomerSerializer(customer, data=data)
        if serializer.is_valid():
            serializer.save()
            return get_response(status.HTTP_200_OK, serializer.data, get_status_msg("UPDATED"))

        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400"))


class ProductsAPI(APIView):

    def get_queryset(self):
        all_products = Product.objects.all()
        return all_products

    def get(self, request):

        all_products = self.get_queryset()
        
        if not all_products: 
            return get_response(status.HTTP_404_NOT_FOUND, [], get_status_msg('DATA_NOT_FOUND'))

        serializer = ProductSerializer(all_products, many = True)
        return get_response(status.HTTP_200_OK, serializer.data, get_status_msg('RETRIEVE'))
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'weight': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request):

        data = request.data
        serializer = ProductSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return get_response(status.HTTP_200_OK, serializer.data, get_status_msg("CREATED"))
        
        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400"))

class OrdersAPI(APIView):

    def get_queryset(self):
        all_orders = Order.objects.all()
        return all_orders

    def get(self, request):

        all_orders = self.get_queryset()
        
        if not all_orders: 
            return get_response(status.HTTP_404_NOT_FOUND, [], get_status_msg('DATA_NOT_FOUND'))

        serializer = OrderSerializer(all_orders, many = True)
        return get_response(status.HTTP_200_OK, serializer.data, get_status_msg('RETRIEVE'))

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer': openapi.Schema(type=openapi.TYPE_INTEGER),
                'order_data': openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request):

        data = request.data

        serializer = OrderSerializer(data = data)

        latest_order = self.get_queryset().order_by('-id').first()

        order_number = Generate_Order_Number(latest_order)
    
        data['order_number'] = order_number
        if serializer.is_valid():
            # serializer.save()
            return get_response(status.HTTP_200_OK, serializer.data, get_status_msg("CREATED"))
        
        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400"))

class OrderItemsAPI(APIView):

    def get_queryset(self):
        all_order_items = Order_item.objects.all()
        return all_order_items

    def get(self, request):

        all_order_items = self.get_queryset()
        
        if not all_order_items: 
            return get_response(status.HTTP_404_NOT_FOUND, [], get_status_msg('DATA_NOT_FOUND'))

        serializer = OrderItemSerializer(all_order_items, many = True)
        return get_response(status.HTTP_200_OK, serializer.data, get_status_msg('RETRIEVE'))
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                'product': openapi.Schema(type=openapi.TYPE_INTEGER),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
    )
    def post(self, request):

        data = request.data
        print("➡ data :", data)
        serializer = OrderItemSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return get_response(status.HTTP_200_OK, serializer.data, get_status_msg("CREATED"))
        
        return get_response(status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400"))

