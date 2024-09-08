from django.db import models


class Product(models.Model):
    """Product items"""

    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Leads(models.Model):
    """Lead Management"""

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
    )
    product = models.ManyToManyField("Product", related_name="interested_products")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"
