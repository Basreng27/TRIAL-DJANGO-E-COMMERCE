from django.db import models

# Create your models here.
class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('DONE', 'Done'),
        ('CANCEL', 'Cancel'),
        ('WAITING', 'Waiting'),
    ]
    
    # customer_id = 
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='WAITING')
    shipping_address = models.TextField()
    
# For Blacklist Token
class BlacklistedToken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)