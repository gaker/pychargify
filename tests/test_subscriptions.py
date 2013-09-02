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

        self.assertEqual(len(subscriptions), 1)

        subscription = subscriptions[0]

        self.assertIsInstance(subscription.customer, Customer)
        self.assertIsInstance(subscription.product, Product)

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
        subscription = obj.get(id=123)

        self.assertIsInstance(subscription.customer, Customer)
        self.assertIsInstance(subscription.product, Product)

    #     self.assertTrue(product.require_credit_card)
