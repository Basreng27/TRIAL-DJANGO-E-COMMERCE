from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import *
from .models import *

# Create your views here.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['email'] = self.user.email

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Ambil token refresh dari header Authorization
            token = request.data.get('refresh')
            if token is None:
                return Response({'detail': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Tambahkan token ke blacklist
            token_blacklist = RefreshToken(token)
            token_blacklist.blacklist()

            return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({'detail': 'Token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    
class BrandCreate(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BrandDetail(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj = Brand.objects.get(id=self.kwargs["id"])
        
        return obj

class BrandUpdate(generics.UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        # Handle PATCH requests
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Handle PUT request
        return self.update(request, *args, **kwargs)

class BrandDelete(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Handle DELETE request
        return self.destroy(request, *args, **kwargs)
    
class ShippingMethods(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Mendapatkan ID dari parameter URL
        shipping_id = kwargs.get('id')
        
        if shipping_id:
            # Mengambil objek tunggal berdasarkan ID
            shipping_method = get_object_or_404(ShippingMethod, id=shipping_id)
            serializer = ShippingMethodSerializers(shipping_method)
            return Response(serializer.data)
        else:
            # Mengambil semua objek
            query = ShippingMethod.objects.all()
            serializer = ShippingMethodSerializers(query, many=True)
            return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = ShippingMethodSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwargs):
            shipping_id = kwargs.get('id')
            shipping_method = get_object_or_404(ShippingMethod, id=shipping_id)
            
            serializer = ShippingMethodSerializers(shipping_method, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        shipping_id = kwargs.get('id')
        shipping_method = get_object_or_404(ShippingMethod, id=shipping_id)
        
        serializer = ShippingMethodSerializers(shipping_method, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        shipping_id = kwargs.get('id')
        shipping_method = get_object_or_404(ShippingMethod, id=shipping_id)
        
        shipping_method.delete()
        
        return Response("OK", status=status.HTTP_200_OK)