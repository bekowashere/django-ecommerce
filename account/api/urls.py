from django.urls import path
from account.api.views import (
    # CUSTOMER
    CustomerRegisterAPIView,
    CustomerProfileUpdateAPIView,
    DefaultAddressUpdateAPIView,
    ListAddressAPIView,
    AddressCreateUpdateDeleteAPIView,
    
    # SELLER
    SellerRegisterAPIView,
    SellerMultipleImagesCreateAPIView,
    SellerCompanyImageUpdateAPIView,
    SellerProfileUpdateAPIView,
    SellerSlugUpdateAPIView,
    SellerCodeUpdateAPIView,
    SellerContactUpdateAPIView,
    SellerLocationUpdateAPIView,
    SellerMultipleImagesCreateAPIViewV2,

    # PASSWORD
    ChangePasswordView    
)

app_name = 'account'

urlpatterns = [
    # CUSTOMER
    path('register/customer/', CustomerRegisterAPIView.as_view(), name='customer_register'),
    path('customer/profile/', CustomerProfileUpdateAPIView.as_view(), name='customer_profile'),
    path('customer/default/address/', DefaultAddressUpdateAPIView.as_view(), name='customer_default_address'),
    path('customer/addresses/', ListAddressAPIView.as_view(), name='list_address'),
    path('customer/address/', AddressCreateUpdateDeleteAPIView.as_view(), name='customer_address'),
    
    # SELLER
    path('register/seller/', SellerRegisterAPIView.as_view(), name='seller_register'),
    path('seller/profile/', SellerProfileUpdateAPIView.as_view(), name='seller_profile'),
    
    path('seller/profile/images/', SellerMultipleImagesCreateAPIView.as_view(), name='seller_profile_images'),
    path('seller/profile/imagesv2/', SellerMultipleImagesCreateAPIViewV2.as_view(), name='seller_profile_imagesv2'),

    path('seller/profile/slug/', SellerSlugUpdateAPIView.as_view(), name='seller_profile_slug'),
    path('seller/profile/code/', SellerCodeUpdateAPIView.as_view(), name='seller_profile_code'),

    path('seller/company_image/', SellerCompanyImageUpdateAPIView.as_view(), name='seller_company_image'),
    path('seller/contact/', SellerContactUpdateAPIView.as_view(), name='seller_contact'),
    path('seller/location/', SellerLocationUpdateAPIView.as_view(), name='seller_location'),

    # PASSWORD
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

]