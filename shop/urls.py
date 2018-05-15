from django.urls import path, include
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('calc_price', views.calc_price, name='calc_price'),
    path('order_add', views.order_add, name='order_add'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('pay_order', views.pay_order, name='pay_order')

]
