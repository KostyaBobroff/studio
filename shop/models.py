from django.db import models
from PIL import Image
import datetime


class Material(models.Model):
    name = models.CharField(max_length=50)
    cost = models.FloatField(verbose_name='Стоимость единицы материала')
    footage = models.FloatField()

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)
    sewing_time = models.TimeField()
    k_length_of_arms = models.FloatField(default=0.0)
    k_length_of_legs = models.FloatField(default=0.0)
    k_length_of_waist_girth = models.FloatField(default=0.0)
    k_length_of_head = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=10, verbose_name='RGB значение')

    def __str__(self):
        return self.name


class Catalog(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material, related_name='catalog_for_material')
    colors = models.ManyToManyField(Color, related_name='catalog_for_color')
    image = models.ImageField(upload_to='photo')

    def __str__(self):
        return ' '.join([self.type.__str__(), self.name])


class OrderItem(models.Model):
    model_from_catalog = models.ForeignKey('Catalog', on_delete=models.CASCADE, related_name='catalog_for_orderItem')
    color = models.ForeignKey('Color', on_delete=models.CASCADE, related_name='color_for_orderItem')
    material = models.ForeignKey('Material', on_delete=models.CASCADE, related_name='material_for_orderItem')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    sewing_cost = models.FloatField(blank=True, null=True)

    def __str__(self):
        return ' '.join['orderItem', str(self.pk)]


STATUS_CHOICE = (
    ('unpaid', 'не оплачено'),
    ('work', 'в работе'),
    ('ready', 'готово')
)


class Order(models.Model):
    price = models.DecimalField(max_digits=32, decimal_places=10, default=0.0)
    client = models.ForeignKey('studio_auth.User', on_delete=models.CASCADE)
    cutter = models.ForeignKey('studio_auth.User', on_delete=models.CASCADE, related_name='orders', blank=True,
                               null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    date_of_completion = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE, default='unpaid', max_length=10)
    active = models.BooleanField(default=True)

    def calc_price(self):
        self.price = 34


def __str__(self):
    return 'Order {}'.format(self.pk)
