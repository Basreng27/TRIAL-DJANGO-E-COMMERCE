from django.urls import path
from . import views

urlpatterns = [
    path('/', views.dashboard, name='dashboard'),
    path('/product', views.product, name='product'),
    path('/category', views.category, name='category'),
]
