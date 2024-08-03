from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        login_url = reverse('login')
        register_url = reverse('register')
        process_login_url = reverse('process-login')

        if token:
            try:
                AccessToken(token)
            except:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            if request.path not in [login_url, register_url, process_login_url]:
                return redirect(login_url)

        response = self.get_response(request)
        return response