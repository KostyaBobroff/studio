from django.urls import path, include
from . import views


urlpatterns = [
    path('cart/', views.cart, name='account.cart'),
    path('orders/', views.orders, name='account.orders'),
    path('bill/<int:order_id>/', views.bill, name='account.bill'),
]
