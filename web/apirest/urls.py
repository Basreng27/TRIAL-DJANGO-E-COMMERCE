from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('brand', BrandList.as_view(), name='brand'),
    path('brand/<int:id>', BrandDetail.as_view(), name='brand-detail'),
    path('brand_create', BrandCreate.as_view(), name='brand-create'),
    path('brand_update/<int:pk>', BrandUpdate.as_view(), name='brand-update'),
    path('brand_delete/<int:pk>', BrandDelete.as_view(), name='brand-delete'),
    
    path('shipping_method', ShippingMethods.as_view(), name='shipping-method'),
    path('shipping_method/<int:id>', ShippingMethods.as_view(), name='shipping-method-detail'),
    
    path('token/login', CustomTokenObtainPairView.as_view(), name='token-login'),
    path('token/logout', Logout.as_view(), name='token-logout'),
    
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]