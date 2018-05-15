from django.contrib import admin

from .models import Order, Material, Type, Color, Catalog, OrderItem
from studio_auth.models import User

# @admin.register(Order)
# class AdminOrder(admin.ModelAdmin):
#     pass

    # def has_add_permission(self, request):
    #     return False
admin.site.register(Order)
admin.site.register(Material)
admin.site.register(Type)
admin.site.register(Color)
admin.site.register(Catalog)
admin.site.register(OrderItem)
#admin.site.register(User)