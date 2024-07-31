from django.shortcuts import render
from .modules.auth.login import login_view

# Create your views here.
def login(request):
    return login_view(request)

def dashboard(request):
    return render(request, 'templates/dashboard.html')