# import requests
from django.shortcuts import render
from .modules.auth.login import page_login, process_login, process_logout
from .modules.auth.register import page_register
from .modules.master.product import page_product, delete_product, form_product
from .modules.master.category import page_category, delete_category, form_category
from .modules.master.brand import page_brand, form_brand, delete_brand
from .modules.master.shipping_method import page_shipping_method, form_shipping_method, delete_shipping_method
from .modules.master.payment_method import page_payment_method, form_payment_method, delete_payment_method
from .modules.guest.pages import initial_page, page_shop, page_shop_detail, page_cart, page_checkout
from .modules.transaction.order import page_order, form_order

def dashboard(request):
    data = {
        'title': "Dashboard"
    }

    return render(request, 'template/dashboard.html', data)

# Auth
def login(request):
    return page_login(request)

def login_process(request):
    return process_login(request)

def logout_process(request):
    return process_logout(request)

def register(request):
    return page_register(request)

# Master Product
def product(request):
    return page_product(request)

def product_form(request, id=None):
    return form_product(request, id)

def product_delete(request, id=None):
    return delete_product(request, id)

# Master Category
def category(request):
    return page_category(request)

def category_form(request, id=None):
    return form_category(request, id)

def category_delete(request, id=None):
    return delete_category(request, id)

# Rest API
# Master Brand
def brand(request):
    return page_brand(request)

def brand_form(request, id=None):
    return form_brand(request, id)

def brand_delete(request, id=None):
    return delete_brand(request, id)

# Master Shipping Method
def shipping_method(request):
    return page_shipping_method(request)

def shipping_method_form(request, id=None):
    return form_shipping_method(request, id)

def shipping_method_delete(request, id=None):
    return delete_shipping_method(request, id)

# Master Brand Rest API
def payment_method(request):
    return page_payment_method(request)

def payment_method_form(request, id=None):
    return form_payment_method(request, id)

def payment_method_delete(request, id=None):
    return delete_payment_method(request, id)

# Transaction
def order(request):
    return page_order(request)

def order_form(request, id=None):
    return form_order(request, id)

# Guest
def page(request):
    return initial_page(request)

def shop(request):
    return page_shop(request)

def shop_detail(request):
    return page_shop_detail(request)

def cart(request):
    return page_cart(request)

def checkout(request):
    return page_checkout(request)