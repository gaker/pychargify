"""
Test Subscription endpoints
"""
import datetime
import json

from httpretty import HTTPretty, httprettified
from nose.tools import raises

from pychargify.api import Subscription, Customer, Product
from .base import TestBase

class TestProducts(TestBase):

    def setUp(self):
        self.subscriptions_list = self.load_fixtures('subscriptions')

    @httprettified
    def test_get_subscription_list(self):
        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://some-test.chargify.com/subscriptions.json",
            body=json.dumps(self.subscriptions_list))

        obj = Subscription('1234', 'some-test')
        subscriptions = obj.get()

        self.assertEqual(len(subscriptions), 2)

        subscription = subscriptions[0]

        self.assertIsInstance(subscription.customer, Customer)
        self.assertIsInstance(subscription.product, Product)
        self.assertIsInstance(subscription.updated_at, datetime.datetime)

    @httprettified
    def test_get_subscription(self):
        """
        Test getting a single subscription
        """
        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://some-test.chargify.com/subscriptions/123.json',
            body=json.dumps(self.subscriptions_list[0])
        )

        obj = Subscription('1234', 'some-test')
        subscription = obj.get(object_id=123)

        self.assertIsInstance(subscription.customer, Customer)
        self.assertIsInstance(subscription.product, Product)

    @httprettified
    def test_get_subscription_by_customer_id(self):
        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://some-test.chargify.com/customers/1/subscriptions.json',
            body=json.dumps([])
        )

        obj = Subscription('1234', 'some-test')
        subscriptions = obj.get(customer_id=1)

        self.assertEqual(len(subscriptions), 0)

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://some-test.chargify.com/customers/12345/subscriptions.json',
            body=json.dumps(self.subscriptions_list)
        )

        obj = Subscription('1234', 'some-test')
        subscriptions = obj.get(customer_id=12345)
        self.assertEqual(len(subscriptions), 2)

    # @httprettified
    # def test_create_subscription(self):
    #     """
    #     Test creating a subscription
    #     """
    #     post_body = {
    #         'subscription': {
    #             'product_handle': 'super-widget-1',
    #             'customer_id': 12345,
    #             'credit_card_attributes': {
    #                 'full_number': "1234",
    #                 'expiration_month': "10",
    #                 'expiration_year': '2020'
    #             }
    #         }
    #     }

    #     HTTPretty.register_uri(
    #         HTTPretty.POST,
    #         'https://some-test.chargify.com/subscriptions.json',
    #         body=json.dumps(self.subscriptions_list[0])
    #     )



    #     # customer = Customer('1234', 'some-test')
    #     # customer.first_name = 'Greg'
    #     # customer.last_name = 'Aker'
    #     # customer.email = 'greg@gregaker.net'
    #     # customer.save()

    #     subscription = Subscription('1234', 'some-test')

