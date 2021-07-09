from django.test import TestCase

from auction.models import Item, Lot
from tests.testing_utilities import ApiUtility


class AuctionProcessTestCase(TestCase):
    def setUp(self):
        self.api_utility = ApiUtility()

        # User
        self.user_seller1 = self.api_utility.register_user()
        self.user_seller2 = self.api_utility.register_user()

        # Customer
        self.user_customer1 = self.api_utility.register_user()
        self.user_customer2 = self.api_utility.register_user()

        # Items
        self.item_of_user_seller1 = self.api_utility.register_item(
            user_id=self.user_seller1.get('id'),
            item_type=Item.EZHIK
        )
        self.item_of_user_seller2 = self.api_utility.register_item(
            user_id=self.user_seller2.get('id'),
            item_type=Item.CAT
        )

    def test_users_creates_lots_to_sell(self):
        """
        1. Пользователи выставляют лоты на продажу
        """
        self.lot_of_user_seller1 = self.api_utility.register_lot(
            user_id=self.user_seller1.get('id'),
            item_id=self.item_of_user_seller1.get('id'),
        )
        self.lot_of_user_seller2 = self.api_utility.register_lot(
            user_id=self.user_seller2.get('id'),
            item_id=self.item_of_user_seller2.get('id'),
        )

        self.assertEqual(self.lot_of_user_seller1.get('owner'), self.user_seller1.get('id'), 'Lot1 created')
        self.assertEqual(self.lot_of_user_seller2.get('owner'), self.user_seller2.get('id'), 'Lot2 created')

        """
        2. Другие пользователи могут сделать ставку на лот
        """
        self.bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.get('id'),
            value=float(self.lot_of_user_seller1.get('cost')) + 1
        )
        self.bet_of_user_customer2 = self.api_utility.register_bet(
            user_id=self.user_customer2.get('id'),
            lot_id=self.lot_of_user_seller2.get('id'),
            value=float(self.lot_of_user_seller2.get('cost')) + 1
        )
        self.assertEqual(self.bet_of_user_customer1.get('owner'), self.user_customer1.get('id'), 'Bet1 created')
        self.assertEqual(self.bet_of_user_customer2.get('owner'), self.user_customer2.get('id'), 'Bet2 created')

        """
        3. Автор лота принимает одну любую ставку
        """
        self.apply_bet_user_seller1 = self.api_utility.apply_bet(
            bet_id=self.bet_of_user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.get('id'),
        )
        self.apply_bet_user_seller2 = self.api_utility.apply_bet(
            bet_id=self.bet_of_user_customer2.get('id'),
            lot_id=self.lot_of_user_seller2.get('id'),
        )

        lot1 = Lot.objects.filter(id=self.lot_of_user_seller1.get('id')).first()
        lot2 = Lot.objects.filter(id=self.lot_of_user_seller2.get('id')).first()

        self.assertEqual(lot1.finished_bet.id, self.bet_of_user_customer1.get('id'), 'Lot1 finished')
        self.assertEqual(lot2.finished_bet.id, self.bet_of_user_customer2.get('id'), 'Lot2 finished')

    def test_less_than_lot_value_bet(self):
        self.lot_of_user_seller1 = self.api_utility.register_lot(
            user_id=self.user_seller1.get('id'),
            item_id=self.item_of_user_seller1.get('id'),
        )
        self.good_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.get('id'),
            value=float(self.lot_of_user_seller1.get('cost')) + 5
        )

        self.bad_bet_of_user_customer1 = self.api_utility.register_bet(
            user_id=self.user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.get('id'),
            value=float(self.lot_of_user_seller1.get('cost')) - 5
        )

        self.good_bet_of_user_customer2 = self.api_utility.register_bet(
            user_id=self.user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.get('id'),
            value=float(self.lot_of_user_seller1.get('cost')) + 6
        )

        self.bad_bet_of_user_customer3 = self.api_utility.register_bet(
            user_id=self.user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.get('id'),
            value=float(self.lot_of_user_seller1.get('cost')) + 4
        )

        self.good_bet_of_user_customer4 = self.api_utility.register_bet(
            user_id=self.user_customer1.get('id'),
            lot_id=self.lot_of_user_seller1.get('id'),
            value=float(self.lot_of_user_seller1.get('cost')) + 4
        )

        self.assertTrue('non_field_errors' not in self.good_bet_of_user_customer1, 'More than cost of Lot')
        self.assertTrue('non_field_errors' in self.bad_bet_of_user_customer1, 'Less than cost of Lot')
        self.assertTrue('non_field_errors' not in self.good_bet_of_user_customer2, 'More than last bet ')
        self.assertTrue('non_field_errors' in self.bad_bet_of_user_customer3, 'Less than last bet')


