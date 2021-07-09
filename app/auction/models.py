from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class OwnerMixin(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Item(OwnerMixin):
    HEDGEHOG = 0
    CAT = 1
    TYPES = [
        (HEDGEHOG, 'Hedgehog'),
        (CAT, 'Cat'),
    ]
    breed = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    type = models.IntegerField(choices=TYPES, default=HEDGEHOG)


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

    def last_bet(self):
        return Bet.objects.order_by('-value')\
            .filter(lot=self.id).first()

    def close_lot(self):
        self.finished_bet = self.last_bet()

        if self.finished_bet is None:
            raise ValueError('You cannot close this lot')

        # Change balance
        self.finished_bet.owner.profile.balance = self.finished_bet.owner.profile.balance - self.finished_bet.value
        self.finished_bet.owner.profile.save()

        self.save()


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
