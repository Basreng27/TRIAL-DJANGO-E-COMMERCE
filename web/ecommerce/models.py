from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class ProductCategoris(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Product Category {self.product_id} by {self.product_id.name}'
class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
class OrderItems(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'OrderItems {self.order_id} by {self.user.username}'
    
class Payments(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    
    def __str__(self):
        return f'OrderItems {self.order_id} by {self.user.username}'