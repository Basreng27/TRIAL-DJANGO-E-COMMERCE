import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Products(models.Model):
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='img/product/', blank=True, null=True)
    # image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
    
# Untuk menghapus file gambar dari sistem file saat produk dihapus
@receiver(models.signals.post_delete, sender=Products)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)