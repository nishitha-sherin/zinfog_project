# customer/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register', views.CustomerRegisterView.as_view(), name='customer-register'),
    path('login', views.CustomerLoginView.as_view(), name='customer-login'),
    path('products', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('address', views.AddressCreateView.as_view(), name='address-create'),
    path('cart', views.CartAddProductView.as_view(), name='cart-add-product'),
    path('order/place', views.OrderPlaceView.as_view(), name='order-place'),
    
]