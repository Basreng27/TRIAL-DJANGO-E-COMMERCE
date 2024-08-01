from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('product', views.product, name='product'),
    path('product_form', views.product_form, name='product-form'),
    path('product_form/<int:id>', views.product_form, name='product-form-update'),
    path('product_delete/<int:id>', views.product_delete, name='product-delete'),
    path('category', views.category, name='category'),
]
