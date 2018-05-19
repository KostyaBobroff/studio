from django.contrib import admin
from django import forms
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from studio_auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest
from shop.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    exclude = ('quantity',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('model_from_catalog', 'color', 'material', 'sewing_cost',)
        return self.readonly_fields


class UserInline(admin.TabularInline):
    model = User


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status',)
    # fields = ('cutter', 'status', 'cutter',)
    inlines = (OrderItemInline,)

    fields = (
        'status', 'cutter',
        (
            'client', 'get_client_length_of_arms', 'get_client_length_of_legs',
            'get_client_length_of_waist_girth', 'get_client_length_of_head'
        ),
        'active', 'price',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(cutter_id=request.user.pk)

    def get_items(self, obj, ):
        return obj.items

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return (
                'cutter', 'client',
                'get_client_length_of_arms', 'get_client_length_of_waist_girth',
                'get_client_length_of_head', 'get_client_length_of_legs',
                'active', 'price'
            ) + self.readonly_fields
        else:
            return self.readonly_fields

    def get_client_length_of_arms(self, obj):
        return obj.client.length_of_arms
    get_client_length_of_arms.short_description = 'Длина рук'

    def get_client_length_of_legs(self, obj):
        return obj.client.length_of_legs
    get_client_length_of_legs.short_description = 'Длина ног'

    def get_client_length_of_waist_girth(self, obj):
        return obj.client.length_of_waist_girth
    get_client_length_of_waist_girth.short_description = 'Обхват талии'

    def get_client_length_of_head(self, obj):
        return obj.client.length_of_head
    get_client_length_of_head.short_description = 'Обхват головы'

    def get_order(self, obj):
        return obj


class CustomUserAdmin(UserAdmin):
    exclude = ('last_login', 'date_joined')
    fieldsets = (
        ('Personal info', {'fields': ('email', 'password', 'first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )


# admin.site.register(User, AdminUser)
admin.site.register(User, CustomUserAdmin)
admin.register(Group)
