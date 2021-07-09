from faker import Faker
from rest_framework.test import APIRequestFactory, APIClient
from core.settings import API_PREFIX


class ApiUtility:
    api_url = 'http://localhost:8000/'

    def __init__(self):
        self.api_client = APIClient()
        self.faker = Faker()

    def register_user(self):
        data = {
            'username': self.faker.first_name(),
            'email': self.faker.email(),
        }
        response = self.api_client.post(f'{self.api_url}{API_PREFIX}users/', data, format='json')
        print(response.json())
        return response.json()
