from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        
        paths = [reverse('page'), reverse('login'), reverse('register'), reverse('process-login'), reverse('shop'), reverse('shop-detail'), reverse('cart'), reverse('checkout')]
        
        if token:
            try:
                AccessToken(token)
            except:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            if request.path not in paths:
                return redirect(paths[1])

        response = self.get_response(request)
        
        return response