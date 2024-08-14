from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from jwt import encode, decode as jwt_decode, exceptions
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from typing import Optional

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
            "id": d.id,
            "name": d.name,
            "description": d.description,
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

class OrderSchema(Schema):
    customer_id: Optional[int] = None
    shipping_id: Optional[int] = None
    order_date: Optional[str] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    shipping_address: Optional[str] = None
    
@api.get('/order', auth=auth)
def PaymentMethodList(request):
    data = Order.objects.all()
    
    return[
        {
            "id": d.id,
            "customer": f'{d.customer_id.first_name} {d.customer_id.first_name}',
            "shipping": d.shipping_id.name,
            "order_date": d.order_date,
            "total_amount": d.total_amount,
            "status": d.status,
            "shipping_address": d.shipping_address,
        }
        # For Loop
        for d in data
    ]
    
@api.post("/order", auth=auth)
def create(request, payload: OrderSchema):
    # Parse order_date
    try:
        order_date = datetime.fromisoformat(payload.order_date)
    except ValueError:
        return {"error": "Invalid date format. Use ISO 8601 format."}
    
    # Get the customer and shipping method objects
    try:
        customer = User.objects.get(id=payload.customer_id)
    except User.DoesNotExist:
        return {"error": "Customer not found."}
    
    try:
        shipping_method = ShippingMethod.objects.get(id=payload.shipping_id)
    except ShippingMethod.DoesNotExist:
        return {"error": "Shipping method not found."}
    
    # data = Order.objects.create(**payload.dict())
    data = Order.objects.create(
        customer_id=customer,
        shipping_id=shipping_method,
        order_date=order_date,
        total_amount=payload.total_amount,
        status=payload.status,
        shipping_address=payload.shipping_address
    )
    
    return {
        "id": data.id,
        "customer": f'{data.customer_id.first_name} {data.customer_id.first_name}',
        "shipping": data.shipping_id.name,
        "order_date": data.order_date,
        "total_amount": data.total_amount,
        "status": data.status,
        "shipping_address": data.shipping_address,
    }

@api.get("/order/{id}", auth=auth)
def get(request, id: int):
    data = get_object_or_404(Order, id=id)
    
    return {
        "id": data.id,
        "customer": f'{data.customer_id.first_name} {data.customer_id.first_name}',
        "shipping": data.shipping_id.name,
        "order_date": data.order_date,
        "total_amount": data.total_amount,
        "status": data.status,
        "shipping_address": data.shipping_address,
    }

@api.put("/order/{id}", auth=auth)
def update(request, id: int, payload: OrderSchema):
    
    # try:
    #     order_date = datetime.fromisoformat(payload.order_date)
    # except ValueError:
    #     return {"error": "Invalid date format. Use ISO 8601 format."}
    
    # try:
    #     customer = User.objects.get(id=payload.customer_id)
    # except User.DoesNotExist:
    #     return {"error": "Customer not found."}
    
    # try:
    #     shipping_method = ShippingMethod.objects.get(id=payload.shipping_id)
    # except ShippingMethod.DoesNotExist:
    #     return {"error": "Shipping method not found."}
    
    order = get_object_or_404(Order, id=id)

    # Update fields dynamically only if they are provided in the payload
    if hasattr(payload, 'status') and payload.status is not None:
        order.status = payload.status

    if hasattr(payload, 'order_date') and payload.order_date is not None:
        # Parse order_date
        try:
            order.order_date = datetime.fromisoformat(payload.order_date)
        except ValueError:
            return {"error": "Invalid date format. Use ISO 8601 format."}

    if hasattr(payload, 'customer_id') and payload.customer_id is not None:
        try:
            customer = User.objects.get(id=payload.customer_id)
            order.customer_id = customer
        except User.DoesNotExist:
            return {"error": "Customer not found."}

    if hasattr(payload, 'shipping_id') and payload.shipping_id is not None:
        # Get the customer and shipping method objects
        try:
            shipping_method = ShippingMethod.objects.get(id=payload.shipping_id)
            order.shipping_id = shipping_method
        except ShippingMethod.DoesNotExist:
            return {"error": "Shipping method not found."}

    if hasattr(payload, 'total_amount') and payload.total_amount is not None:
        order.total_amount = payload.total_amount

    if hasattr(payload, 'shipping_address') and payload.shipping_address is not None:
        order.shipping_address = payload.shipping_address
    
    order.save()
    
    return {
        "id": order.id,
        "customer": f'{order.customer_id.first_name} {order.customer_id.last_name}',
        "shipping": order.shipping_id.name,
        "order_date": order.order_date,
        "total_amount": order.total_amount,
        "status": order.status,
        "shipping_address": order.shipping_address,
    }

@api.delete("/order/{id}", auth=auth)
def delete(request, id: int):
    data = get_object_or_404(Order, id=id)
    
    data.delete()
    
    return {"message": "Deleted successfully"}
