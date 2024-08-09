from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout', views.logout_process, name='logout'),
    
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
    
    # Rest API
    # Master Brand
    path('brand', views.brand, name='brand-restapi'),
    path('brand_form', views.brand_form, name='brand-restapi-form'),
    path('brand_form/<int:id>', views.brand_form, name='brand-restapi-update'),
    path('brand_delete/<int:id>', views.brand_delete, name='brand-restapi-delete'),
    # Master Shipping Method
    path('shipping_method', views.shipping_method, name='shipping-method-restapi'),
    path('shipping_method_form', views.shipping_method_form, name='shipping-method-restapi-form'),
    path('shipping_method_form/<int:id>', views.shipping_method_form, name='shipping-method-restapi-update'),
    path('shipping_method_delete/<int:id>', views.shipping_method_delete, name='shipping-method-restapi-delete'),
    
    # Master Payment Method From Rest API
    path('payment_method', views.payment_method, name='payment-method-ninjaapi'),
    path('payment_method_form', views.payment_method_form, name='payment-method-ninjaapi-form'),
    path('payment_method_form/<int:id>', views.payment_method_form, name='payment-method-ninjaapi-update'),
    path('payment_method_delete/<int:id>', views.payment_method_delete, name='payment-method-ninjaapi-delete'),
    
    # guest
    path('shop', views.page_shop, name='shop'),
    path('shop_detail', views.page_shop_detail, name='shop-detail'),
    path('cart', views.page_cart, name='cart'),
    path('checkout', views.page_checkout, name='checkout'),
]
