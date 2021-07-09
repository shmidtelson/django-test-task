from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class OwnerMixin(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Item(OwnerMixin):
    EZHIK = 0
    CAT = 1
    TYPES = [
        (EZHIK, 'Ezhik'),
        (CAT, 'Cat'),
    ]
    breed = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    type = models.CharField(max_length=3, choices=TYPES, default=EZHIK)


class Lot(OwnerMixin):
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    finished_bet = models.ForeignKey(
        'Bet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bet_finished'
    )


class Bet(OwnerMixin):
    value = models.DecimalField(max_digits=6, decimal_places=2)
    lot = models.ForeignKey('Lot', on_delete=models.SET_NULL, null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return "%s's profile" % self.user

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
