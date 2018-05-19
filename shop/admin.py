from django.contrib import admin

from .models import Order, Material, Type, Color, Catalog, OrderItem
from studio_auth.models import User

admin.site.register(Material)
admin.site.register(Type)
admin.site.register(Color)
admin.site.register(Catalog)
admin.site.register(OrderItem)
