from decimal import Decimal

from faker import Faker
from rest_framework.test import APIClient

from auction.models import Profile
from core.settings import API_PREFIX


class ApiUtility:
    api_url = 'http://localhost:8000/'

    def __init__(self):
        self.api_client = APIClient()
        self.faker = Faker()

    def register_user(self) -> dict:
        data = {
            'username': self.faker.first_name(),
            'email': self.faker.email(),
        }

        return self.__register(data, 'users')

    def register_lot(self, user_id: int, item_id: int) -> dict:
        data = {
            "item": item_id,
            "cost": self.faker.pydecimal(left_digits=3, right_digits=2, positive=True),
            "owner": user_id,
        }

        return self.__register(data, 'lots')

    def register_item(self, user_id: int, item_type: int) -> dict:
        data = {
            "breed": self.faker.first_name(),
            "nickname": self.faker.first_name(),
            "owner": user_id,
            "type": item_type,
        }

        return self.__register(data, 'items')

    def register_bet(self, user_id: int, lot_id: int, value: float = None) -> dict:
        data = {
            "value": value if value else self.faker.pydecimal(left_digits=3, right_digits=2, positive=True),
            "owner": user_id,
            "lot": lot_id
        }
        return self.__register(data, 'bets')

    def apply_bet(self, lot_id: int, bet_id: int):
        data = {
            'finished_bet': bet_id,
        }

        response = self.api_client.patch(
            f'{self.__get_endpoint("lots")}{lot_id}/',
            data,
            format='json'
        )

        return response.json()

    @staticmethod
    def update_balance(user_id: int, balance):
        Profile.objects.filter(user_id=user_id) \
            .update(balance=Decimal(balance))

    def __register(self, data: dict, endpoint: str) -> dict:
        response = self.api_client.post(self.__get_endpoint(endpoint), data, format='json')

        return response.json()

    def __get_endpoint(self, endpoint_name: str):
        return f'{self.api_url}{API_PREFIX}{endpoint_name}/'
