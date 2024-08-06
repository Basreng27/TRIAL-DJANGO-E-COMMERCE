from rest_framework import serializers
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description']

class ShippingMethodSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['name', 'description']