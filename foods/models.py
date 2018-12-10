from django.db import models
from django.utils import timezone
from django.conf import settings


class Food(models.Model):
    code = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=500, null=True)
    product_name = models.CharField(max_length=255, null=True)
    brands = models.CharField(max_length=255, null=True)
    quantity = models.CharField(max_length=255, null=True)
    categories_fr = models.TextField(null=True)
    image_url = models.TextField(max_length=255, null=True)
    nutrition_grade_fr = models.CharField(max_length=1, null=True)
    countries_fr = models.CharField(max_length=255, null=True)
    fat_100g = models.FloatField(null=True)
    saturated_fat_100g = models.FloatField(null=True)
    sugars_100g = models.FloatField(null=True)
    salt_100g = models.FloatField(null=True)
    author = models.ManyToManyField(settings.AUTH_USER_MODEL)
    substitute = models.ManyToManyField('self')

    def __str__(self):
        return self.product_name or 'no name'
