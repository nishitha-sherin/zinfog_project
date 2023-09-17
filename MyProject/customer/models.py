
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.forms import JSONField

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trash = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.JSONField(null=True)  
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True)
    products = JSONField(null = True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=zip(range(1, 6), range(1, 6)))
    review_text = models.TextField(blank=True)

    def __str__(self):
        return f"Review by {self.customer.user.username} for {self.product.name}"

