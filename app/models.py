from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25.0)],
    )

    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_number = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    order_data = models.DateField()
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.order_number + " " + self.customer.name

class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.order.customer.name + " " + self.id
    