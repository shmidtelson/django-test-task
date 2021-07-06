from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser
)


class OwnerMixin(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Customer(AbstractBaseUser):
    balance = models.DecimalField(max_digits=6, decimal_places=2)


class Item(OwnerMixin):
    breed = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)


class Lot(OwnerMixin):
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)


class Bet(OwnerMixin):
    value = models.DecimalField(max_digits=6, decimal_places=2)
