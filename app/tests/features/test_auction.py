from django.contrib.auth.models import User
from django.test import TestCase
from tests.testing_utilities import ApiUtility


class AuctionProcessTestCase(TestCase):
    def setUp(self):
        self.api_utility = ApiUtility()
        user1 = self.api_utility.register_user()
        print(user1)
        print(User.objects.all())
        pass
        # self.user_seller1 = User.objects.create(name='John')
        # self.user_seller2 = User.objects.create(name='John')
        #
        # self.user_customer1 = User.objects.create(name='John')
        # self.user_customer2 = User.objects.create(name='John')

    def test_users_creates_lots_to_sell(self):
        """
        1. Пользователи выставляют лоты на продажу
        """
        self.assertTrue(0)

    def test_other_users_can_do_bet_to_lot(self):
        """
        2. Другие пользователи могут сделать ставку на лот
        """
        pass

    def test_author_of_lot_apply_one_any_bet(self):
        """
        3. Автор лота принимает одну любую ставку
        """
        pass
