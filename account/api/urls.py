from django.urls import path
from account.api.views import (
    # CUSTOMER
    CustomerRegisterAPIView,
    ListAddressAPIView,
    AddressCreateUpdateDeleteAPIView
)

app_name = 'account'

urlpatterns = [
    # CUSTOMER
    path('register/customer/', CustomerRegisterAPIView.as_view(), name='customer_register'),
    path('addresses/', ListAddressAPIView.as_view(), name='list_address'),
    path('customer/create/address/', AddressCreateUpdateDeleteAPIView.as_view(), name='create_address'),
]