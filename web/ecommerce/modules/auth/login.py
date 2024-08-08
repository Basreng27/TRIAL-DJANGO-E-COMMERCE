import json
import requests
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
                restapi_tokens = get_token_apirest(username, password)
                ninjaapi_tokens = get_token_apininja(username, password)
                
                tokens = get_token(user)
                response = HttpResponse(response_success('ecommerce', 'Login', 'Anda Berhasil Login'))
                response.set_cookie('access_token', tokens['access'], httponly=True)
                response.set_cookie('access_token_api_rest', restapi_tokens['access'], httponly=True)
                response.set_cookie('access_token_api_ninja', ninjaapi_tokens['token'], httponly=True)
                
                return response
            else:
                return response_failed('Login', 'Username Atau Password Salah')
        else:
            return response_failed('Login', 'Username Atau Password Kosong')
    
    return redirect('login')

def get_token_apirest(username, password):
    url = 'http://localhost:8000/apirest/token/login'
    data = {'username': username, 'password': password}
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_token_apininja(username, password):
    url = 'http://localhost:8000/apininja/login'
    data = {'username': username, 'password': password}
    
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        return response.json()
    else:
        return None

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