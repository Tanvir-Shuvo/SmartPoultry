from django.conf import settings
from django.db import models


# ============================================================
# FARM MODEL
# ============================================================
# Stores the basic information of a poultry farm.
# One User can own multiple Farms.
# ============================================================

class Farm(models.Model):

    FARM_TYPES = [
        ("BROILER", "Broiler"),
        ("LAYER", "Layer"),
        ("SONALI", "Sonali"),
        ("MIXED", "Mixed"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="farms",
    )

    name = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=255
    )

    farm_type = models.CharField(
        max_length=10,
        choices=FARM_TYPES,
    )

    capacity = models.PositiveIntegerField()

    start_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_farm_name_per_owner",
            ),
        ]

    def __str__(self):
        return self.name


# ============================================================
# BATCH MODEL
# ============================================================
# Stores a group of poultry within a specific farm.
# One Farm can have multiple Batches.
# A Batch represents a group of birds started together.
# ============================================================

class Batch(models.Model):

    POULTRY_TYPES = [
        ("BROILER", "Broiler"),
        ("LAYER", "Layer"),
        ("SONALI", "Sonali"),
        ("OTHER", "Other"),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="batches",
    )

    code = models.CharField(
        max_length=50
    )

    poultry_type = models.CharField(
        max_length=10,
        choices=POULTRY_TYPES,
    )

    start_date = models.DateField()

    initial_bird_count = models.PositiveIntegerField()

    purchase_price_per_bird = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    is_active = models.BooleanField(
        default=True
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["farm", "code"],
                name="unique_batch_code_per_farm",
            ),
        ]

    def __str__(self):
        return self.code


# ============================================================
# DAILY RECORD MODEL
# ============================================================

class DailyRecord(models.Model):

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="daily_records",
    )

    record_date = models.DateField()

    feed_amount_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    water_liters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    dead_count = models.PositiveIntegerField(
        default=0
    )

    sick_count = models.PositiveIntegerField(
        default=0
    )

    medicine_used = models.BooleanField(
        default=False
    )

    medicine_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "record_date"],
                name="unique_daily_record_per_batch_date",
            ),
        ]

    def __str__(self):
        return f"{self.batch.code} - {self.record_date}"


# ============================================================
# EGG PRODUCTION MODEL
# ============================================================

class EggProduction(models.Model):

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="egg_productions",
    )

    production_date = models.DateField()

    egg_count = models.PositiveIntegerField()

    damaged_egg_count = models.PositiveIntegerField(
        default=0
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "production_date"],
                name="unique_egg_production_per_batch_date",
            ),
        ]

    @property
    def good_egg_count(self):
        return self.egg_count - self.damaged_egg_count

    def __str__(self):
        return f"{self.batch.code} - {self.production_date}"


# ============================================================
# EXPENSE MODEL
# ============================================================

class Expense(models.Model):

    EXPENSE_TYPES = [
        ("FARM", "Farm"),
        ("BATCH", "Batch"),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="expenses",
        blank=True,
        null=True,
    )

    expense_type = models.CharField(
        max_length=5,
        choices=EXPENSE_TYPES,
    )

    category = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    expense_date = models.DateField()

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.category} - {self.amount}"


# ============================================================
# SALE MODEL
# ============================================================

class Sale(models.Model):

    SALE_TYPES = [
        ("POULTRY", "Poultry"),
        ("EGG", "Egg"),
    ]

    SALE_UNITS = [
        ("BIRD", "Bird"),
        ("EGG", "Egg"),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="sales",
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="sales",
    )

    sale_type = models.CharField(
        max_length=10,
        choices=SALE_TYPES,
    )

    unit = models.CharField(
        max_length=5,
        choices=SALE_UNITS,
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    sale_date = models.DateField()

    buyer_name = models.CharField(
        max_length=200,
        blank=True,
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.sale_type} - {self.quantity}"