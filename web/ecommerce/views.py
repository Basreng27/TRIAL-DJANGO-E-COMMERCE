from django.shortcuts import render
from .modules.auth.login import page_login, process_login, process_logout
from .modules.auth.register import page_register
from .modules.master.product import page_product, delete_product, form_product
from .modules.master.category import page_category, delete_category, form_category

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