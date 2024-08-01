from django.shortcuts import render
from .modules.auth.login import login_view
from .modules.master.product import product_view
from .modules.master.category import category_view

def dashboard(request):
    data = {
        'title': "Dashboard"
    }
    
    return render(request, 'template/dashboard.html', data)

# Auth
def login(request):
    return login_view(request)

# Master Product
def product(request):
    return product_view(request)

# Master Category
def category(request):
    return category_view(request)