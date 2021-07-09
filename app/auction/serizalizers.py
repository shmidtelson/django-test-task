from django.contrib.auth.models import User
from rest_framework import serializers

from auction.models import Item, Lot, Bet, Profile
from auction.service.bet_validate_service import BetValidateService


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('balance',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'profile', 'is_staff', 'url', 'username', 'email',)
        read_only_fields = ('id', 'profile', 'is_staff',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'breed', 'nickname', 'owner', 'type',)


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('id', 'value', 'owner', 'lot',)

    def validate(self, data):
        bet_validate_service = BetValidateService(data)
        bet_validate_service.validate()
        return data


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ('id', 'item', 'cost', 'owner', 'finished_bet',)
