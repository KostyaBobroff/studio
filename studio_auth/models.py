from django.contrib.auth.models import AbstractUser
from django.db import models

from shop.models import Catalog, Material


class User(AbstractUser):
    phone = models.IntegerField(null=True)
    # orders_count = models.ManyToManyField(Order)
    length_of_arms = models.FloatField(default=0.0, verbose_name='Длина рук')
    length_of_legs = models.FloatField(default=0.0, verbose_name='Длина ног')
    length_of_waist_girth = models.FloatField(default=0.0, verbose_name='Обхавт туловища')
    length_of_head = models.FloatField(default=0.0, verbose_name='Обхват головы')

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])

    def get_material_footage(self, model_id):
        model = Catalog.objects.get(pk=model_id)
        catalog_type = model.type

        arms = catalog_type.k_length_of_arms * self.length_of_arms
        legs = catalog_type.k_length_of_legs * self.length_of_legs
        waist_girth = catalog_type.k_length_of_waist_girth * self.length_of_waist_girth
        head = catalog_type.k_length_of_head * self.length_of_head
        return arms + legs + waist_girth + head

    def calc_price(self, material_id, model_id):
        material = Material.objects.get(pk=material_id)
        return self.get_material_footage(model_id) * material.cost
