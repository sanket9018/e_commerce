from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db.models import Sum
from . models import (
    Customer,
    Product,
    Order,
    Order_item,
)
from django.utils import timezone
from datetime import date

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'contact_number',
            'email',
        ]

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'weight',
        ]
    
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order_item
        fields = [
            'id',
            'order',
            'product',
            'quantity',
        ]

    def validate(self, value):
        print("➡ value :", value)
        order = value['order'].id
        product = value['product'].id
        quantity = value['quantity']
        order_obj = Order.objects.filter(id = order).first()
        product_obj = Product.objects.filter(id = product).first()

        if not order_obj or not product_obj:
            raise serializers.ValidationError("Invalid order or product.")

        total_weight = product_obj.weight * quantity
        current_order_weight = Order_item.objects.filter(order=order).aggregate(Sum('product__weight'))['product__weight__sum']
        print("➡ current_order_weight :", current_order_weight)

        if current_order_weight is None:
            current_order_weight = 0

        if (current_order_weight + total_weight) > 150.0:
            raise serializers.ValidationError("Order cumulative weight exceeds 150kg.")

        return value

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(read_only = True, many = True)
    class Meta:
        model = Order
        depth = 1
        fields = [
            'id',
            'customer',
            'order_data',
            'order_number',
            'address',
            'order_items',
        ]
    
    def validate_order_data(self, value):
        if value <  date.today():
            raise serializers.ValidationError("Date must not be in the past.")
        return value
