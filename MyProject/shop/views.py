# shop/views.py

from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializer import ProductSerializer
from customer.models import Order
from customer.serializers import OrderSerializer
from django.shortcuts import render

class ShopLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer  # Use the appropriate serializer for User model
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopOrderRetrieveUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        order = self.get_object(pk)
        data = request.data
        if 'status' in data:
            # Update the status of the order
            order.status = data['status']
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response({'status': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
def dashboard_view(request):
    orders = Order.objects.all()
    return render(request, 'shop/dashboard.html', {'orders': orders})