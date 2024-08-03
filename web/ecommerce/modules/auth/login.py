from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from ...form import LoginForm
from ...helpers import response_success, response_failed

def page_login (request):
    form = LoginForm(request.POST or None)
    
    data = {
        'form': form,
        'url_action': reverse('process-login')
    }
    
    return render(request, 'auth/login.html', data)

def process_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') # Get Username
        password = request.POST.get('password') # Get Password
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                tokens = get_token(user)
                response = HttpResponse(response_success('ecommerce', 'Login', 'Anda Berhasil Login'))
                response.set_cookie('access_token', tokens['access'], httponly=True)
                
                return response
            else:
                return response_failed('Login', 'Username Atau Password Salah')
        else:
            return response_failed('Login', 'Username Atau Password Kosong')
    
    return redirect('login')

def get_token(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def process_logout(request):
    response = HttpResponse(response_success('login', 'Logout', 'Anda Berhasil Logout'))
    response.delete_cookie('access_token')
    
    # Optional: revoke refresh token if available
    refresh_token = request.COOKIES.get('refresh_token')
    
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return response_failed('Logout','Failed to blacklist refresh token')
    
    return response