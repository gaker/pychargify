"""
Test customer endpoint
"""

import datetime
import json
import unittest
from httpretty import HTTPretty
from pychargify.api import Customer


class TestCustomer(unittest.TestCase):
    """
    Test customer endpoints
    """
    customer_list = [
        {
            u'customer': {
                u'city': u'Columbia',
                u'first_name': u'Greg',
                u'last_name': u'Aker',
                u'zip': u'65202',
                u'reference': u'greg1',
                u'country': u'US',
                u'created_at': u'2013-04-02T23:43:19-04:00',
                u'updated_at': u'2013-06-30T16:29:00-04:00',
                u'id': 12345,
                u'phone': u'',
                u'state': u'MO',
                u'address_2': u'',
                u'address': u'123 My Street',
                u'organization': u'',
                u'email': u'me@foobar.com'
            }
        }
    ]

    def test_get_customers(self):
        """
        Test fetching a list of users.
        """
        HTTPretty.enable()
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
