from django.contrib.auth.models import User
from django.test import TestCase

from auction.models import Item, Lot
from tests.testing_utilities import ApiUtility


class AuctionProcessTestCase(TestCase):
    fixtures = [
        "tests/fixtures/auction.json",
    ]

    def setUp(self):
        self.api_utility = ApiUtility()

        # User
        self.user_seller1 = User.objects.get(username='seller_1')
        self.user_seller2 = User.objects.get(username='seller_2')

        # Customer
        self.user_customer1 = User.objects.get(username='customer_1')
        self.user_customer2 = User.objects.get(username='customer_2')

        # Items
        self.item_of_user_seller1 = Item.objects.get(owner=self.user_seller1.id)
        self.item_of_user_seller2 = Item.objects.get(owner=self.user_seller2.id)

        # Lots
        self.lot_of_user_seller1 = Lot.objects.get(owner=self.user_seller1.id)  # type: Lot
        self.lot_of_user_seller2 = Lot.objects.get(owner=self.user_seller2.id)  # type: Lot

        # Update balance
        self.api_utility.update_balance(self.user_customer1.id, 1000)
        self.api_utility.update_balance(self.user_customer2.id, 1000)

    def test_users_creates_lots_to_sell(self):
        """
        1. Пользователи выставляют лоты на продажу
        """
        self.assertEqual(self.lot_of_user_seller1.owner.id, self.user_seller1.id, 'Lot1 created')
        self.assertEqual(self.lot_of_user_seller2.owner.id, self.user_seller2.id, 'Lot2 created')

        """
        2. Другие пользователи могут сделать ставку на лот
        """
        self.bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 1
        )
        self.bet_of_user_customer2 = self.api_utility.register_bet(
            user_id=self.user_customer2.id,
            lot_id=self.lot_of_user_seller2.id,
            value=float(self.lot_of_user_seller2.cost) + 1
        )
        self.assertEqual(self.bet_of_user_customer1.get('owner'), self.user_customer1.id, 'Bet1 created')
        self.assertEqual(self.bet_of_user_customer2.get('owner'), self.user_customer2.id, 'Bet2 created')

        """
        3. Автор лота принимает одну любую ставку
        """
        self.apply_bet_user_seller1 = self.api_utility.apply_bet(
            bet_id=self.bet_of_user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.id,
        )
        self.apply_bet_user_seller2 = self.api_utility.apply_bet(
            bet_id=self.bet_of_user_customer2.get('id'),
            lot_id=self.lot_of_user_seller2.id,
        )

        lot1 = Lot.objects.filter(id=self.lot_of_user_seller1.id).first()
        lot2 = Lot.objects.filter(id=self.lot_of_user_seller2.id).first()

        self.assertEqual(lot1.finished_bet.id, self.bet_of_user_customer1.get('id'), 'Lot1 finished')
        self.assertEqual(lot2.finished_bet.id, self.bet_of_user_customer2.get('id'), 'Lot2 finished')

    def test_less_than_lot_value_bet(self):
        """
        Ставки больше или меньше стоимости лота или последней ставки
        """
        self.good_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 5
        )

        self.bad_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) - 5
        )

        self.good_bet_of_user_customer2 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 6
        )

        self.bad_bet_of_user_customer3 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 4
        )

        self.good_bet_of_user_customer4 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 4
        )

        self.assertTrue('non_field_errors' not in self.good_bet_of_user_customer1, 'More than cost of Lot')
        self.assertTrue('non_field_errors' in self.bad_bet_of_user_customer1, 'Less than cost of Lot')
        self.assertTrue('non_field_errors' not in self.good_bet_of_user_customer2, 'More than last bet ')
        self.assertTrue('non_field_errors' in self.bad_bet_of_user_customer3, 'Less than last bet')

    def test_not_enough_money(self):
        self.api_utility.update_balance(self.user_customer1.id, 1000)

        self.good_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 5
        )

        self.api_utility.update_balance(self.user_customer1.id, 1)

        self.bad_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 5
        )

        self.assertTrue('non_field_errors' not in self.good_bet_of_user_customer1, 'enough Money')
        self.assertTrue('non_field_errors' in self.bad_bet_of_user_customer1, 'Not enough Money')

    def test_closed_lot(self):
        self.api_utility.update_balance(self.user_customer1.id, 1000)

        self.good_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 5
        )
        self.lot_of_user_seller1.close_lot()

        self.bad_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=float(self.lot_of_user_seller1.cost) + 5
        )

        self.assertTrue('non_field_errors' not in self.good_bet_of_user_customer1, 'enough Money')
        self.assertTrue('non_field_errors' in self.bad_bet_of_user_customer1, 'Not enough Money')

    def test_changed_balance(self):
        started_balance = 1000
        bet_value = float(self.lot_of_user_seller1.cost) + 5

        self.api_utility.update_balance(self.user_customer1.id, 1000)

        self.good_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.id,
            lot_id=self.lot_of_user_seller1.id,
            value=bet_value
        )
        self.lot_of_user_seller1.close_lot()

        self.assertEqual(float(self.user_customer1.profile.balance), started_balance - bet_value, 'balance changed')
