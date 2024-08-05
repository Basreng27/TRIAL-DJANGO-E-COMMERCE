from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('brand', BrandList.as_view(), name='brand'),
    
    path('token/login', CustomTokenObtainPairView.as_view(), name='token-login'),
    path('token/logout', Logout.as_view(), name='token-logout'),
    
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]