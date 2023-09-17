from django.urls import path
from . import views

urlpatterns = [
    path('login', views.ShopLoginView.as_view(), name='shop-login'),
    path('products', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('shop-order/<int:pk>/', views.ShopOrderRetrieveUpdateView.as_view(), name='shop-order-detail'),
]
