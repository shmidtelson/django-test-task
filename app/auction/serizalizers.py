from django.contrib.auth.models import User
from rest_framework import serializers

from auction.models import Item, Lot, Bet, Profile


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
        if data.get('value') <= data.get('lot').cost:
            raise serializers.ValidationError("Bet value doesnt be less or equal than lot cost")

        last_bet = Bet.objects.order_by('-value').filter(lot=data.get('lot').id).first()

        if last_bet and data.get('value') <= last_bet.value:
            raise serializers.ValidationError("Bet value doesnt be less or equal than last bet")
        return data


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ('id', 'item', 'cost', 'owner', 'finished_bet',)
