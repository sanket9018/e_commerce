from django.urls import path
from app.views import (
    CustomersAPI,
    CustomersUpdateAPI,
    ProductsAPI,
    OrdersAPI,
    OrdersUpdateAPI,
)

urlpatterns = [
    path("api/customers/", CustomersAPI.as_view(), name="create-customers"),
    path(
        "api/customers/<int:id>/", CustomersUpdateAPI.as_view(), name="update-customers"
    ),
    path("api/products/", ProductsAPI.as_view(), name="create-products"),
    path("api/orders/", OrdersAPI.as_view(), name="create-orders"),
    path("api/orders/<int:id>/", OrdersUpdateAPI.as_view(), name="update-orders"),
]
