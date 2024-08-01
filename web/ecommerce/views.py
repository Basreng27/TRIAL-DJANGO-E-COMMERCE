from django.shortcuts import render
from .modules.auth.login import login_view
from .modules.master.product import product_view

def dashboard(request):
    data = {
        'title': "Dashboard"
    }
    
    return render(request, 'template/dashboard.html', data)

# Auth
def login(request):
    return login_view(request)

# Master
def product(request):
    return product_view(request)