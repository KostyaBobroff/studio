import random

from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from shop.models import *
from studio_auth.models import User
from django.contrib.auth.decorators import login_required
from decimal import *
from datetime import timedelta


@login_required(login_url='/auth/login')
def index(request):
    catalog = []
    user = request.user
    for c in Catalog.objects.all():
        material_footage = user.get_material_footage(c.id)
        materials = c.materials.filter(footage__gte=material_footage) #list(filter(lambda m: m.footage >= material_footage, c.material.all()))
        catalog.append({
            'id': c.id,
            'materials': materials,
            'colors': c.colors,
            'image': c.image,
            'name': c.name,
            'type': c.type
        })
    price = 'Выберите материал'
    return render(request, 'shop/index.html', {'catalog': catalog, 'price': price})


@login_required(login_url='/auth/login')
def calc_price(request):
    material_id = int(request.GET.get('material'))
    model_id = int(request.GET.get('model'))
    return JsonResponse({
        'price': request.user.calc_price(material_id, model_id)
    })


@login_required(login_url='/auth/login')
def order_add(request):
    pass


@login_required(login_url='/auth/login')
def add_to_cart(request):
    order = Order.objects.filter(client_id=request.user.pk, active=True).first()
    if order is not None:
        item = OrderItem.objects.create(model_from_catalog_id=int(request.GET.get('model')),
                                        material_id=int(request.GET.get('material')),
                                        color_id=int(request.GET.get('color')),
                                        quantity=1,
                                        order_id=order.pk)
        item.sewing_cost = Decimal(request.user.calc_price(item.material_id, item.model_from_catalog_id))
        item.order = order
        item.save()
        order.price = order.price + item.sewing_cost
        print(order.price)
        time = item.model_from_catalog.type.sewing_time
        order.date_of_completion += timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        order.save()
    else:
        order = Order.objects.create(client_id=request.user.pk, active=True)
        order.save()
        item = OrderItem.objects.create(model_from_catalog_id=int(request.GET.get('model')),
                                        material_id=int(request.GET.get('material')),
                                        color_id=int(request.GET.get('color')),
                                        quantity=1,
                                        order_id=order.pk)
        item.sewing_cost = Decimal(request.user.calc_price(item.material_id, item.model_from_catalog_id))
        item.order = order
        item.save()
        order.price = Decimal(item.sewing_cost)
        print(order.price)
        time = item.model_from_catalog.type.sewing_time
        order.date_of_completion += timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        order.save()
    return HttpResponseRedirect("/shop")


@login_required(login_url='/auth/login')
def pay_order(request):
    order_id = int(request.POST.get('order_id'))
    order = Order.objects.get(id=order_id)
    order.active = False
    order.order_date = datetime.datetime.now()
    order.status = 'work'
    order.cutter_id = int(request.POST.get('cutter'))
    order.save()
    return redirect('account.orders')
