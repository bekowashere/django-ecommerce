from django.urls import path
from store.api.views import (
    ProductCreateUpdateAPIView,
    ProductInventoryCreateUpdateAPIView
)

app_name = 'store'

urlpatterns = [
    path('product/create/', ProductCreateUpdateAPIView.as_view(), name='product_create'),
    path('inventory/create/', ProductInventoryCreateUpdateAPIView.as_view(), name='inventory_create'),

]