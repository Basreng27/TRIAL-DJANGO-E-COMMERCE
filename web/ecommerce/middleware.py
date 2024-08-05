from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model # Get User Login
from apirest.urls import *

User = get_user_model()

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        
        paths = [
            reverse('page'), 
            reverse('login'), 
            reverse('logout'),
            reverse('register'), 
            reverse('process-login'), 
            reverse('shop'), 
            reverse('shop-detail'), 
            reverse('cart'), 
            reverse('checkout'), 
            reverse('token_obtain_pair'), 
            reverse('token_refresh'),
            reverse('brand'),
            reverse('token-login'),
            reverse('token-logout'),
        ]
        
        if token:
            try:
                # Decode the token
                access_token = AccessToken(token)
                # Retrieve the user id from the token
                user_id = access_token['user_id']
                # Set the user to the request
                request.user = User.objects.get(id=user_id)
            except Exception as e:
                # Token is invalid, return a 401 response
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            # If the path is not in the allowed list, redirect to login
            if request.path not in paths:
                return redirect('login')

        # If user is not set, set it to AnonymousUser
        if not hasattr(request, 'user'):
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()

        response = self.get_response(request)
        
        return response