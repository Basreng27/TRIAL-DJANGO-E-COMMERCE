from rest_framework import serializers
from .models import *

class BrandSerializers(serializers.Serializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description']

class ShippingMethodSerializers(serializers.Serializer):
    class Meta:
        model = ShippingMethod
        fields = ['name', 'description']