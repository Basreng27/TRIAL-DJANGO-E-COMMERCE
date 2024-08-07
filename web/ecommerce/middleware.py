from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model # Get User Login
from django.utils.deprecation import MiddlewareMixin
from apirest.urls import *
from django.http import HttpResponseRedirect

User = get_user_model()

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the path is part of the API
        
        if request.path.startswith('/apirest/') or request.path.startswith('/apininja/'):
            # Process API authentication
            token = request.COOKIES.get('access_token') or request.headers.get('Authorization')
            
            if token:
                if token.startswith('Bearer '):
                    token = token.split(' ')[1]

                if request.path.startswith('/apirest/'):
                    try:
                        access_token = AccessToken(token)
                        user_id = access_token['user_id']
                        request.user = User.objects.get(id=user_id)
                    except Exception:
                        return JsonResponse({'error': 'Invalid token'}, status=401)
            else:
                if request.path not in [
                    reverse('token_obtain_pair'), 
                    reverse('token_refresh'),
                    reverse('token-login'),
                    '/apininja/login',
                ]:
                    return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)
        else:
            # Process web authentication
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
            ]
            
            if token:
                try:
                    access_token = AccessToken(token)
                    user_id = access_token['user_id']
                    request.user = User.objects.get(id=user_id)
                except Exception:
                    response = HttpResponseRedirect('/login')
                    response.delete_cookie('access_token') # Hapus cookie
                    
                    return response
            else:
                if request.path not in paths:
                    return redirect('login')

        if not hasattr(request, 'user'):
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()

        return self.get_response(request)