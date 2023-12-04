from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .utils import get_response, get_status_msg, Generate_Order_Number

from .models import (
    Customer,
    Product,
    Order,
)

from .serializer import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
)


class CustomersAPI(APIView):
    def get_queryset(self):
        all_customers = Customer.objects.all()
        return all_customers

    def get(self, request):
        all_customers = self.get_queryset()

        if not all_customers:
            return get_response(
                status.HTTP_404_NOT_FOUND, [], get_status_msg("DATA_NOT_FOUND")
            )

        serializer = CustomerSerializer(all_customers, many=True)
        return get_response(
            status.HTTP_200_OK, serializer.data, get_status_msg("RETRIEVE")
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "contact_number": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request):
        data = request.data
        serializer = CustomerSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return get_response(
                status.HTTP_200_OK, serializer.data, get_status_msg("CREATED")
            )

        return get_response(
            status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400")
        )


class CustomersUpdateAPI(APIView):
    def get_queryset(self, id):
        customer = Customer.objects.filter(id=id).first()
        return customer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "contact_number": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def put(self, request, id):
        customer = self.get_queryset(id)
        if not customer:
            return get_response(
                status.HTTP_404_NOT_FOUND, {}, get_status_msg("DATA_NOT_FOUND")
            )

        data = request.data

        serializer = CustomerSerializer(customer, data=data)
        if serializer.is_valid():
            serializer.save()
            return get_response(
                status.HTTP_200_OK, serializer.data, get_status_msg("UPDATED")
            )

        return get_response(
            status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400")
        )


class ProductsAPI(APIView):
    def get_queryset(self):
        all_products = Product.objects.all()
        return all_products

    def get(self, request):
        all_products = self.get_queryset()

        if not all_products:
            return get_response(
                status.HTTP_404_NOT_FOUND, [], get_status_msg("DATA_NOT_FOUND")
            )

        serializer = ProductSerializer(all_products, many=True)
        return get_response(
            status.HTTP_200_OK, serializer.data, get_status_msg("RETRIEVE")
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "weight": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return get_response(
                status.HTTP_200_OK, serializer.data, get_status_msg("CREATED")
            )

        return get_response(
            status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400")
        )


class OrdersAPI(APIView):
    def get_queryset(self):
        all_orders = Order.objects.all()
        return all_orders

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "products",
                openapi.IN_QUERY,
                description="List of products separated by commas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "customer",
                openapi.IN_QUERY,
                description="Customer name",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of orders", schema=OrderSerializer(many=True)
            ),
            404: "Not Found",
        },
    )
    def get(self, request):
        products_param = request.query_params.get("products", None)
        customer_param = request.query_params.get("customer", None)

        if products_param:
            orders = Order.objects.filter(
                order_items__product__name__in=products_param.split(",")
            ).distinct()
        elif customer_param:
            orders = Order.objects.filter(customer__name=customer_param)
        else:
            orders = self.get_queryset()

        if not orders:
            return get_response(
                status.HTTP_404_NOT_FOUND, [], get_status_msg("DATA_NOT_FOUND")
            )

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "customer": openapi.Schema(type=openapi.TYPE_INTEGER),
                "order_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                "address": openapi.Schema(type=openapi.TYPE_STRING),
                "order_items": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "product": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                ),
            },
        )
    )
    def post(self, request, format=None):
        data = request.data

        serializer = OrderSerializer(data=data)
        latest_order = self.get_queryset().order_by("-id").first()

        order_number = Generate_Order_Number(latest_order)

        data["order_number"] = order_number

        if serializer.is_valid():
            serializer.save()
            return get_response(
                status.HTTP_200_OK, serializer.data, get_status_msg("CREATED")
            )

        return get_response(
            status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400")
        )


class OrdersUpdateAPI(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "customer": openapi.Schema(type=openapi.TYPE_INTEGER),
                "order_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                "address": openapi.Schema(type=openapi.TYPE_STRING),
                "order_items": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "product": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                ),
            },
        )
    )
    def put(self, request, id, format=None):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return get_response(
                status.HTTP_404_NOT_FOUND, {}, get_status_msg("DATA_NOT_FOUND")
            )

        data = request.data
        serializer = OrderSerializer(instance=order, data=data)

        data["order_number"] = order.order_number

        if serializer.is_valid():
            serializer.save()
            return get_response(
                status.HTTP_200_OK, serializer.data, get_status_msg("UPDATED")
            )

        return get_response(
            status.HTTP_400_BAD_REQUEST, serializer.errors, get_status_msg("ERROR_400")
        )
