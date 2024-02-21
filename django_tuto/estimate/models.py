from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postal_code = models.IntegerField()
    type_of_property = models.CharField(max_length=100)
    type_of_sale = models.CharField(max_length=100)
    kitchen = models.CharField(max_length=100)
    state_of_building = models.CharField(max_length=100)
    bedrooms = models.IntegerField(null=True, blank=True)
    surface_of_good = models.FloatField(null=True, blank=True)
    number_of_facades = models.IntegerField(null=True, blank=True)
    living_area = models.FloatField()
    garden_area = models.FloatField(null=True, blank=True)
    estimation = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.living_area}m² à {self.postal_code} -> {self.estimation:.2f}€"
