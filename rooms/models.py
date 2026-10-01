from django.db import models
from django.conf import settings

# Create your models here.
class UtilityType(models.TextChoices):
    WATER = 'water', 'Вода'
    GAS = 'gas', 'Газ'
    ELECTRICITY = 'electricity', 'Електрика'


class Building(models.Model):
    street = models.CharField(max_length=255)

    def __str__(self):
        return self.street


class Room(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='rooms',
    )
    number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.building.street} — {self.number}"


class Tenant(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tenant_profile',
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lease(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='leases',
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='leases',
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant} in {self.room} from {self.start_date}"


class Tariff(models.Model):
    utility_type = models.CharField(max_length=50, choices=UtilityType.choices)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=4)
    effective_from = models.DateField()

    def __str__(self):
        return f"{self.utility_type}: {self.price_per_unit} з {self.effective_from}"


class UtilityReading(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='utility_readings',
    )
    reading_date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    utility_type = models.CharField(max_length=50, choices=UtilityType.choices)
    consumption = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.room} — {self.utility_type}: {self.value}"


