from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Foods(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    brands = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    nutrition_grades = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    substitute = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('delete', kwargs={'pk': self.pk})
