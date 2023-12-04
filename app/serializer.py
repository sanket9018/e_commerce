from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db.models import Sum
from .models import (
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
            "id",
            "name",
            "contact_number",
            "email",
        ]

    def validate_name(self, value):
        if Customer.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"{value} name is already exists")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "weight",
        ]

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"{value} is already exists in products")
        return value

    def validate_weight(self, value):
        if value < 0 or value > 25:
            raise serializers.ValidationError(
                "Weight can not be less then 0 or more then 25kg"
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_item
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "order_date",
            "address",
            "order_items",
        ]

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            Order_item.objects.create(order=order, **order_item_data)

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("order_items")
        instance.customer = validated_data.get("customer", instance.customer)
        instance.order_date = validated_data.get("order_date", instance.order_date)
        instance.address = validated_data.get("address", instance.address)

        for order_item_data in order_items_data:
            product = order_item_data["product"]
            quantity = order_item_data["quantity"]
            Order_item.objects.update_or_create(
                order=instance, product=product, defaults={"quantity": quantity}
            )

        instance.save()
        return instance

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Date must not be in the past.")
        return value

    def validate(self, value):
        total_weight = sum(
            [prod["product"].weight * prod["quantity"] for prod in value["order_items"]]
        )
        if total_weight > 150:
            raise ValidationError("In a order wight can not be more than 150kg.")
        return value

    def validate_order_items(self, order_items_data):
        product_set = set()
        for order_item_data in order_items_data:
            product = order_item_data["product"]
            if product in product_set:
                raise serializers.ValidationError(f"{product} is already in the order.")
            product_set.add(product)

        return order_items_data
