"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from ecommerce import views
from apininja.api import api

urlpatterns = [
    path('', views.page, name='page'),
    path('login', views.login, name='login'),
    path('process_login', views.login_process, name='process-login'),
    path('register', views.register, name='register'),
    path('ecommerce/', include('ecommerce.urls'), name='ecommerce'),
    path('apirest/', include('apirest.urls'), name='apirest'),
    path('apininja/', api.urls, name='apininja'),
]

# Get Url Image
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)