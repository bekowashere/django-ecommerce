from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView
from account.api.views import (
    MyTokenObtainPairView,
    CustomerMyTokenObtainPairView,
    SellerMyTokenObtainPairView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/account/', include('account.api.urls')),

    # TOKEN - LOGIN
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/customer/', CustomerMyTokenObtainPairView.as_view(), name='login_customer'),
    path('api/login/seller/', SellerMyTokenObtainPairView.as_view(), name='login_seller'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
