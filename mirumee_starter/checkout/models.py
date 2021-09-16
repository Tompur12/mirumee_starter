from django.db import models
from django.conf import settings

from ..product.models import ProductVariant


class Checkout(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='checkouts',
        on_delete=models.CASCADE)
    user_email = models.EmailField()

    def __str__(self):
        return f'{self.user_email}:{self.id}'


class CheckoutLine(models.Model):
    variant = models.ForeignKey(ProductVariant, related_name='variant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    checkout = models.ForeignKey(Checkout, related_name='lines', on_delete=models.CASCADE)
