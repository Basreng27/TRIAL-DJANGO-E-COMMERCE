from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from jwt import encode, decode as jwt_decode, exceptions
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

api = NinjaAPI()

# Auth
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # Cek apakah token ada di daftar hitam
        if BlacklistedToken.objects.filter(token=token).exists():
            return None
        
        try:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            return User.objects.get(id=decoded_data['user_id'])
        except (exceptions.DecodeError, User.DoesNotExist):
            return None

auth = AuthBearer()

# Login
class LoginSchema(Schema):
    username: str
    password: str
    
@api.post("/login")
def login(request, payload:LoginSchema):
    try:
        username = payload.username
        password = payload.password

        user = authenticate(username=username, password=password)
        if user is None:
            return {"error": "Username or password is incorrect"}
        
        # Set expiration time (1 hour from now)
        expiration = datetime.utcnow() + timedelta(hours=1)
        token = encode({
            'user_id': user.id,
            'exp': expiration
        }, settings.SECRET_KEY, algorithm='HS256')

        return {"username": user.username, "email": user.email, "token": token}
    except User.DoesNotExist:
        return {"error": "Password Or Username Wrong!"}
    
@api.post("/logout", auth=auth)
def logout(request):
    token = request.headers.get("Authorization").split(" ")[1]
    BlacklistedToken.objects.create(token=token)
    
    return {"message": "Successfully logged out"}

# Payment Method 
class PaymentMethodSchema(Schema):
    name: str
    description: str
    
@api.get('/payment_method', auth=auth)
def PaymentMethodList(request):
    data = PaymentMethod.objects.all()
    
    return[
        {
            "id":d.id,
            "name":d.name,
            "description":d.description,
        }
        # For Loop
        for d in data
    ]
    
@api.post("/payment_method", auth=auth)
def create(request, data: PaymentMethodSchema):
    data = PaymentMethod.objects.create(name=data.name, description=data.description)
    
    return {"id": data.id, "name": data.name, "description": data.description}

@api.get("/payment_method/{id}", auth=auth)
def get(request, id: int):
    data = get_object_or_404(PaymentMethod, id=id)
    
    return {"id": data.id, "name": data.name, "description": data.description}

@api.put("/payment_method/{id}", auth=auth)
def update(request, id: int, data: PaymentMethodSchema):
    d = get_object_or_404(PaymentMethod, id=id)

    d.name = data.name
    d.description = data.description
    d.save()
    
    return {"id": d.id, "name": d.name, "description": d.description}

@api.delete("/payment_method/{id}", auth=auth)
def delete(request, id: int):
    data = get_object_or_404(PaymentMethod, id=id)
    
    data.delete()
    
    return {"message": "Deleted successfully"}
