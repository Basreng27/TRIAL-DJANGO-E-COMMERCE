from django.shortcuts import render

def page_login (request):
    return render(request, 'auth/login.html')