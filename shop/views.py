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
    # if request.GET:
    #     if not request.GET.get('material_id'):
    #         print('all good')
    #         if Order.objects.filter(client_id=request.user.pk).exists() and Order.objects.get(active=True):
    #             order = Order.objects.get(client_id=request.user.pk)
    #             item = OrderItem.objects.create(catalog_id=int(request.GET.get('model')),
    #                                             material_id=int(request.GET.get('material')),
    #                                             color_id=int(request.GET.get('color')),
    #                                             quantity=1,
    #                                             order_id=Order.objects.get(client_id=request.user.pk).pk)
    #             item.sewing_cost = (item.catalog.type.k_lenght_of_arms * request.user.lenght_of_arms +
    #                                 item.catalog.type.k_lenght_of_head * request.user.lenght_of_head +
    #                                 item.catalog.type.k_lenght_of_trunk * request.user.lenght_of_trunk +
    #                                 item.catalog.type.k_lenght_of_legs * request.user.lenght_of_legs
    #                                 ) * item.material.cost
    #             item.order = order
    #             item.save()
    #
    #             order.price = order.price + Decimal(item.sewing_cost)
    #             print(order.price)
    #             time = item.catalog.type.sewing_time
    #             order.date_of_completion += timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    #             order.save()
    #         else:
    #             order = Order.objects.create(cutter_id=request.GET.get('cutter'), client_id=request.user.pk,
    #                                          active=True)
    #             item = OrderItem.objects.create(catalog_id=int(request.GET.get('model')),
    #                                             material_id=int(request.GET.get('material')),
    #                                             color_id=int(request.GET.get('color')),
    #                                             quantity=1,
    #                                             order_id=Order.objects.get(client_id=request.user.pk).pk)
    #             item.order = order
    #             item.sewing_cost = (item.catalog.type.k_lenght_of_arms * request.user.lenght_of_arms +
    #                                 item.catalog.type.k_lenght_of_head * request.user.lenght_of_head +
    #                                 item.catalog.type.k_lenght_of_trunk * request.user.lenght_of_trunk +
    #                                 item.catalog.type.k_lenght_of_legs * request.user.lenght_of_legs
    #                                 ) * item.material.cost
    #             item.save()
    #             order.price = Decimal(item.sewing_cost)
    #             print(order.price)
    #             time = item.catalog.type.sewing_time
    #             order.date_of_completion += timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    #             order.save()
    #     else:
    #         print('yes material changed')
    #         return HttpResponse({'price': 0.0}, content_type='text/html')

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
