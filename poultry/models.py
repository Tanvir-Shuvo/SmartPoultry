from django.conf import settings
from django.db import models


class Farm(models.Model):
    FARM_TYPES = [
        ("broiler", "Broiler"),
        ("layer", "Layer"),
        ("sonali", "Sonali"),
        ("other", "Other"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="farms",
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    farm_type = models.CharField(
        max_length=20,
        choices=FARM_TYPES,
    )
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name