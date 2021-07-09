from rest_framework import serializers

from auction.models import Bet, Profile


class BetValidateService:
    def __init__(self, data: dict):
        self.data = data

    def validate(self):
        self.__validate_lot_cost_and_bet_value()
        self.__validate_bet_value_and_last_bet_value()
        self.__validate_enough_money()
        self.__validate_closed_lot()

    def __validate_lot_cost_and_bet_value(self):
        if self.data.get('value') <= self.data.get('lot').cost:
            raise serializers.ValidationError("Bet value doesnt be less or equal than lot cost")

    def __validate_bet_value_and_last_bet_value(self):
        last_bet = self.data.get('lot').last_bet()

        if last_bet and self.data.get('value') <= last_bet.value:
            raise serializers.ValidationError("Bet value doesnt be less or equal than last bet")

    def __validate_enough_money(self):
        profile = Profile.objects.get(user_id=self.data.get('owner'))

        if profile.balance < self.data.get('lot').cost:
            raise serializers.ValidationError("Your Balance isn't enough")

    def __validate_closed_lot(self):
        if self.data.get('lot').finished_bet:
            raise serializers.ValidationError("Lot was close")
