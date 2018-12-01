from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Foods(models.Model):
    code = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=500, null=True)
    product_name = models.CharField(max_length=255, null=True)
    brands = models.CharField(max_length=255, null=True)
    quantity = models.CharField(max_length=255, null=True)
    categories_fr = models.TextField(null=True)
    image_url = models.TextField(max_length=255, null=True)
    nutrition_grade_fr = models.CharField(max_length=1, null=True)
    countries_fr = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ManyToManyField(User)
    substitute = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['nutrition_grade_fr']

    def __str__(self):
        return self.name
