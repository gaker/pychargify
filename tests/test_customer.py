"""
Test customer endpoint
"""
from __future__ import unicode_literals
import datetime
import json
import unittest

from httpretty import HTTPretty, httprettified
from nose.tools import raises

from pychargify.api import Customer
from pychargify.exceptions import ChargifyNotFound


class TestCustomer(unittest.TestCase):
    """
    Test customer endpoints
    """
    customer_list = [
        {
            'customer': {
                'city': 'Columbia',
                'first_name': 'Greg',
                'last_name': 'Aker',
                'zip': '65202',
                'reference': 'greg1',
                'country': 'US',
                'created_at': '2013-04-02T23:43:19-04:00',
                'updated_at': '2013-06-30T16:29:00-04:00',
                'id': 12345,
                'phone': '',
                'state': 'MO',
                'address_2': '',
                'address': '123 My Street',
                'organization': '',
                'email': 'me@foobar.com'
            }
        }
    ]

    @httprettified
    def test_get_customers(self):
        """
        Test fetching a list of users.
        """
        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://some-test.chargify.com/customers.json",
            body=json.dumps(self.customer_list))

        obj = Customer('1234', 'some-test')
        customers = obj.get()

        self.assertEqual(len(customers), 1)
        user = customers[0]

        self.assertIsInstance(user.created_at, datetime.datetime)
        self.assertIsInstance(user.updated_at, datetime.datetime)

        for k, v in self.customer_list[0]['customer'].items():
            if k not in ('created_at', 'updated_at'):
                self.assertTrue(hasattr(user, k))
                self.assertEqual(getattr(user, k), v)

    @httprettified
    def test_get_customer(self):
        """
        Test getting a specific customer
        """

        person = self.customer_list[0]

        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://some-test.chargify.com/customers/12345.json",
            body=json.dumps(person)
        )

        obj = Customer('1234', 'some-test')
        customer = obj.get(object_id=12345)

        self.assertEqual(customer.id, person.get('customer').get('id'))

    @httprettified
    @raises(ChargifyNotFound)
    def test_get_invalid_customer(self):
        """
        Attempting to fetch a customer that does not exist should
        raise a :class:`ChargifyNotFound` exception
        """
        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://some-test.chargify.com/customers/1.json",
            status=404
        )

        obj = Customer('1234', 'some-test')
        obj.get(object_id=1)

    @httprettified
    def test_create_customer(self):
        """
        Test creating a new customer
        """
        body = {"customer": {
            "id": 1234,
            "first_name": "John",
            "last_name": "Coltrane",
            "email": "john@example.com",
            "address": "247 Candlewood Path",
            "city": "Dix Hills",
            "state": "NY",
            "zip": '11746',
            "country": "USA",
            "phone": '555-555.1212',
            "reference": "trane"
        }}

        HTTPretty.register_uri(
            HTTPretty.POST,
            "https://some-test.chargify.com/customers.json",
            content_type='application/json',
            body=json.dumps(body),
            status=201
        )

        customer = Customer('1234', 'some-test')
        customer.first_name = "John"
        customer.last_name = "Coltrane"
        customer.email = "john@example.com"
        customer.address = "247 Candlewood Path"
        customer.city = "Dix Hills"
        customer.state = "NY"
        customer.zip = '11746'
        customer.country = "USA"
        customer.phone = '555-555.1212'
        customer.reference = "trane"
        customer.save()

        self.assertEqual(customer.id, 1234)

    @httprettified
    def test_update_customer(self):
        """
        Test updating a customer record
        """

        person = self.customer_list[0]

        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://some-test.chargify.com/customers/12345.json",
            body=json.dumps(person)
        )

        obj = Customer('1234', 'some-test')
        customer = obj.get(object_id=12345)

        updated_person = person.copy()
        updated_person['reference'] = 'foobar'

        HTTPretty.register_uri(
            HTTPretty.PUT,
            "https://some-test.chargify.com/customers/12345.json",
            content_type='application/json',
            body=json.dumps(updated_person),
            status=200
        )

        customer.reference = 'foobar'
        obj = customer.save()

    @httprettified
    def test_get_by_reference(self):
        """
        Test getting a user by reference.
        """
        person = self.customer_list[0]
        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://some-test.chargify.com/customers/lookup.json?reference=greg1",
            body=json.dumps(person)
        )

        obj = Customer('1234', 'some-test')
        customer = obj.get_by_reference('greg1')

        self.assertEqual(customer.id, person['customer']['id'])
