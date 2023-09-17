from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from .models import CustomerProfile
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Product , Cart , Order ,Address, Customer
from .serializers import CartSerializer, OrderSerializer, AddressSerializer
from shop.serializer import ProductSerializer
import requests

class CustomerRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            password=hashed_password,
        )
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class CustomerLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProductListView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated,]
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class CartAddProductView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressCreateView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save() 
            
            Customer.objects.get_or_create(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderPlaceView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        address_id = request.data.get('address_id') 
        try:
            selected_address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return Response({'error': 'Invalid address ID'}, status=status.HTTP_400_BAD_REQUEST)

        customer = request.user
        cart = customer.cart_set.all()  
        order = Order(customer=customer, shipping_address=selected_address)
        order.save()

        
        for item in cart:
            order.products.add(item.product)

        
        cart.delete()

        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

def product_list(request):

    response = requests.get('http://127.0.0.1:8000/customer/products')
    if response.status_code == 200:
        products = response.json() 
    else:
        products = [] 

    return render(request, 'customer/product.html', {'products': products})