# customer/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Cart, Order, Address, Review, Customer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Use the built-in User model
        fields = ('id', 'username', 'email')  # Include relevant fields


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        return Cart.objects.create(products= validated_data.get('products'),quantity= validated_data.get('quantity'))

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
