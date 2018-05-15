from django.contrib import admin
from django import forms
from django.contrib.admin import AdminSite

from studio_auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest
from shop.models import OrderItem

class MyAdminSite(AdminSite):
    site_header = 'Cutter'


admin_site = MyAdminSite(name='myadmin')


class CutterUser(admin.ModelAdmin):
    # add_form = UserCreationForm
    # fieldsets = (
    #     ('Информация', {
    #         'fields': (
    #             ('username', 'password'),
    #             ('is_staff', 'is_superuser'),
    #             ('email', 'phone')
    #         )
    #     }),
    #     ('Размеры', {
    #         'fields': (
    #             ('length_of_arms', 'length_of_legs'),
    #             ('length_of_waist_girth', 'length_of_head')
    #         )
    #     }),
    # )

    list_display = ['model_from_catalog', 'color', 'material', 'order']
    #list_editable = ['order',]
    readonly_fields = ['model_from_catalog',]

admin_site.register(OrderItem, CutterUser)

# admin_site.register(Order,request)
# class UserCreationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#        # fields = ('email',)
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
#
#
# @admin.register(User)
# class AdminUser(admin.ModelAdmin):
#     #add_form = UserCreationForm
#     fieldsets = (
#         ('Информация', {
#             'fields': (
#                 ('username', 'password'),
#                 ('is_staff', 'is_superuser'),
#                 ('email', 'phone')
#             )
#         }),
#         ('Размеры', {
#             'fields': (
#                 ('length_of_arms', 'length_of_legs'),
#                 ('length_of_waist_girth', 'length_of_head')
#             )
#         }),
#     )

# class MyUSerAdmin(UserAdmin):
#     exclude = ('last_login', 'date_joined')
class CustomUserAdmin(UserAdmin):
    exclude = ('last_login', 'date_joined')
    fieldsets = (
        ('Personal info', {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


# admin.site.register(User, AdminUser)
admin.site.register(User, CustomUserAdmin)
