from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Order
from studio_auth.models import User


@login_required(login_url='/auth/login')
def cart(request):
    order = Order.objects.filter(client_id=request.user.pk, active=True).first()
    cutters = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'account/cart.html', {'order': order, 'cutters': cutters})


@login_required(login_url='/auth/login')
def orders(request):
    items = Order.objects.filter(client_id=request.user.pk, active=False)
    return render(request, 'account/orders.html', {'orders': items})


@login_required(login_url='/auth/login')
def bill(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'account/bill.html', {'o': order})
