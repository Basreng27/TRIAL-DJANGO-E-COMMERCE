from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Master Product
    path('product', views.product, name='product'),
    path('product_form', views.product_form, name='product-form'),
    path('product_form/<int:id>', views.product_form, name='product-form-update'),
    path('product_delete/<int:id>', views.product_delete, name='product-delete'),
    
    # Master Category
    path('category', views.category, name='category'),
    path('category_form', views.category_form, name='category-form'),
    path('category_form/<int:id>', views.category_form, name='category-form-update'),
    path('category_delete/<int:id>', views.category_delete, name='category-delete'),
]
