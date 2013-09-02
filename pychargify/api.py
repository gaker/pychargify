# -*- coding: utf-8 -*-
'''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


Created on Nov 20, 2009
Author: Paul Trippett (paul@pyhub.com)
'''
from .exceptions import (
    ChargifyError, ChargifyUnAuthorized,
    ChargifyForbidden, ChargifyNotFound,
    ChargifyUnProcessableEntity, ChargifyServerError
)

import models


class Customer(models.Model):
    """
    Represents Chargify Customers

    See http://docs.chargify.com/api-customers

    """
    id = models.ChargifyField()
    first_name = models.ChargifyField()
    last_name = models.ChargifyField()
    email = models.ChargifyField()
    city = models.ChargifyField()
    address = models.ChargifyField()
    address_2 = models.ChargifyField()
    state = models.ChargifyField()
    zip = models.ChargifyField()
    country = models.ChargifyField()
    phone = models.ChargifyField()
    organization = models.ChargifyField()
    reference = models.ChargifyField()
    created_at = models.ChargifyDateField()
    updated_at = models.ChargifyDateField()

    class Meta:
        url = 'customers.json'
        key = 'customer'

    def __unicode__(self):
        return u'({0}) {1} {2}'.format(
            self.reference, self.first_name, self.last_name)

    # def get(self, id=None):
    #     """
    #     Get a list of customers, or a customer by their internal id.
    #     """
    #     if not id:
    #         customers = self._get('customers.json')
    #         customer_list = set()
    #         for customer in customers:
    #             customer_list.add(self.parse_fields(customer, 'customer'))
    #         return list(customer_list)

    #     customer = self._get('customers/{0}.json'.format(str(id)))
    #     return self.parse_fields(customer, 'customer')

    # def get_by_reference(self, reference):
    #     customer = self._get(
    #         'customers/lookup.json?reference={0}'.format(reference)
    #     )
    #     return self.parse_fields(customer, 'customer')

    # # def get_subscriptions(self):
    # #     obj = ChargifySubscription(self.api_key, self.sub_domain)
    # #     return obj.getByCustomerId(self.id)

    # def save(self):
    #     if self.id:
    #         url = 'customers/{0}.json'.format(self.id)
    #     else:
    #         url = 'customers.json'
    #     customer = self._save(url, 'customer')
    #     return self.parse_fields(customer, 'customer')


# class Product(models.Model):
#     """
#     Represents Chargify Products
#     """
#     __name__ = 'Product'
#     __attribute_types__ = {}
#     __fields__ = [
#         'id', 'price_in_cents', 'name', 'handle', 'description',
#         'product_family', 'accounting_code', 'interval_unit', 'interval',
#         'initial_charge_in_cents', 'trial_price_in_cents', 'trial_interval',
#         'trial_interval_unit', 'expiration_interval', 'archived_at',
#         'expiration_interval_unit', 'return_url', 'created_at', 'updated_at',
#     ]

#     id = None
#     price_in_cents = 0
#     name = None
#     handle = None
#     description = None
#     product_family = {}
#     accounting_code = None
#     interval_unit = 'day'  # month or day
#     interval = 30
#     initial_charge_in_cents = 0
#     trial_price_in_cents = 0
#     trial_interval = 0
#     trial_interval_unit = 'day'  # month or day
#     expiration_interval = 0
#     expiration_interval_unit = 'day'  # month or day
#     return_url = ''
#     require_credit_card = True
#     created_at = None
#     updated_at = None
#     archived_at = None

#     def __repr__(self):
#         return '<{0} {1}>'.format(
#             self.__name__, self.name
#         )

#     def get(self, id=None):
#         """
#         Get a list of Products or a single product
#         """
#         if not id:
#             products = self._get('products.json')
#             product_list = set()
#             for product in products:
#                 product_list.add(self.parse_fields(product, 'product'))
#             return list(product_list)

#         product = self._get('products/{0}.json'.format(id))
#         return self.parse_fields(product, 'product')

#     def save(self):
#         return self._save('products', 'product')

    # def getByHandle(self, handle):
    #     return self._applyS(self._get('/products/handle/' + str(handle) +
    #         '.xml'), self.__name__, 'product')

    # def getPaymentPageUrl(self):
    #     return ('https://' + self.request_host + '/h/' +
    #         self.id + '/subscriptions/new')

    # def getPriceInDollars(self):
    #     return round(float(self.price_in_cents) / 100, 2)

    # def getFormattedPrice(self):
    #     return "$%.2f" % (self.getPriceInDollars())


# class Usage(object):
#     def __init__(self, id, memo, quantity):
#         self.id = id
#         self.quantity = int(quantity)
#         self.memo = memo


# class Subscription(models.Model):
#     """
#     Represents Chargify Subscriptions
#     """
#     id = None
#     activated_at = None
#     created_at = None
#     balance_in_cents = None
#     cancel_at_end_of_period = None
#     canceled_at = None
#     cancellation_message = None
#     coupon_code = None
#     credit_card = None
#     current_period_ends_at = None
#     current_period_started_at = None
#     customer = None
#     delayed_cancel_at = None
#     expires_at = None
#     next_assessment_at = None
#     payment_collection_method = None
#     previous_state = None
#     product = None
#     signup_payment_id = None
#     signup_revenue = None
#     state = None
#     total_revenue_in_cents = None
#     trial_ended_at = None
#     trial_started_at = None
#     updated_at = None

#     class Meta:
#         url = 'subscriptions.json'
#         attribute_types = {
#             'customer': 'ChargifyCustomer',
#             'product': 'ChargifyProduct',
#             'credit_card': 'ChargifyCreditCard'
#         }

#     def __unicode__(self):
#         return u'{0}-{1}'.format(self.product, self.customer)

#     def get(self, id=None):
#         if not id:
#             subscriptions = self._get('subscriptions.json')
#             subscriptions_list = set()
#             for subscription in subscriptions:
#                 subscriptions_list.add(
#                     self.parse_fields(subscription, 'subscription'))

#             return list(subscriptions_list)

#         subscriptions = self._get('subscriptions/{0}.json'.format(id))
#         return self.parse_fields(subscription, 'subscription')

#     def createUsage(self, component_id, quantity, memo=None):
#         """
#         Creates usage for the given component id.
#         """

#         data = '''<?xml version="1.0" encoding="UTF-8"?><usage>
#             <quantity>%d</quantity><memo>%s</memo></usage>''' % (
#                 quantity, memo or "")

#         dom = minidom.parseString(self.fix_xml_encoding(
#             self._post('/subscriptions/%s/components/%d/usages.xml' % (
#                 str(self.id), component_id), data)))

#         return [Usage(*tuple(chain.from_iterable([[x.data
#             for x in i.childNodes] or [None] for i in n.childNodes])))
#             for n in dom.getElementsByTagName('usage')]

#     def getByCustomerId(self, customer_id):
#         return self._applyA(self._get('/customers/' + str(customer_id) +
#             '/subscriptions.xml'), self.__name__, 'subscription')

#     def getBySubscriptionId(self, subscription_id):
#         #Throws error if more than element is returned
#         i, = self._applyA(self._get('/subscriptions/' + str(subscription_id) +
#             '.xml'), self.__name__, 'subscription')
#         return i

#     def save(self):
#         return self._save('subscriptions', 'subscription')

#     def resetBalance(self):
#         self._put("/subscriptions/" + self.id + "/reset_balance.xml", "")

#     def reactivate(self):
#         self._put("/subscriptions/" + self.id + "/reactivate.xml", "")

#     def upgrade(self, toProductHandle):
#         xml = """<?xml version="1.0" encoding="UTF-8"?>
#   <subscription>
#     <product_handle>%s</product_handle>
#   </subscription>""" % (toProductHandle)
#         #end improper indentation

#         return self._applyS(self._put("/subscriptions/" + self.id + ".xml",
#             xml), self.__name__, "subscription")

#     def unsubscribe(self, message):
#         xml = """<?xml version="1.0" encoding="UTF-8"?>
# <subscription>
#   <cancellation_message>
#     %s
#   </cancellation_message>
# </subscription>""" % (message)

#         self._delete("/subscriptions/" + self.id + ".xml", xml)


# class CreditCard(models.Model):
#     """
#     Represents Chargify Credit Cards
#     """
#     __name__ = 'CreditCard'
#     __attribute_types__ = {}

#     first_name = ''
#     last_name = ''
#     full_number = ''
#     masked_card_number = ''
#     expiration_month = ''
#     expiration_year = ''
#     cvv = ''
#     type = ''
#     billing_address = ''
#     billing_city = ''
#     billing_state = ''
#     billing_zip = ''
#     billing_country = ''
#     zip = ''

#     def __init__(self, apikey, subdomain, nodename=''):
#         super(ChargifyCreditCard, self).__init__(apikey, subdomain)
#         if nodename:
#             self.__xmlnodename__ = nodename

#     def save(self, subscription):
#         path = "/subscriptions/%s.xml" % (subscription.id)

#         data = u"""<?xml version="1.0" encoding="UTF-8"?>
#   <subscription>
#     <credit_card_attributes>
#       <full_number>%s</full_number>
#       <expiration_month>%s</expiration_month>
#       <expiration_year>%s</expiration_year>
#       <cvv>%s</cvv>
#       <first_name>%s</first_name>
#       <last_name>%s</last_name>
#       <zip>%s</zip>
#     </credit_card_attributes>
#   </subscription>""" % (self.full_number, self.expiration_month,
#           self.expiration_year, self.cvv, self.first_name,
#           self.last_name, self.zip)
#         # end improper indentation

#         return self._applyS(self._put(path, data),
#             self.__name__, "subscription")


class PostBack(models.Model):
    """
    Represents Chargify API Post Backs
    """
    subscriptions = []

    def __init__(self, apikey, subdomain, postback_data):
        super(PostBack, self).__init__(apikey, subdomain)
        if postback_data:
            self._process_postback_data(postback_data)

    def _process_postback_data(self, data):
        """
        Process the Json array and fetches the Subscription Objects
        """
        csub = ChargifySubscription(self.api_key, self.sub_domain)
        postdata_objects = json.loads(data)
        for obj in postdata_objects:
            self.subscriptions.append(csub.getBySubscriptionId(obj))


class Chargify(object):
    """
    The Chargify class provides the main entry point to the Chargify API
    """
    api_key = ''
    sub_domain = ''

    def __init__(self, api_key=None, sub_domain=None, cred_file=None):
        '''
        We take either an api_key and sub_domain, or a path
        to a file with JSON that defines those two, or we throw
        an error.
        '''
        if api_key and sub_domain:
            self.api_key = api_key
            self.sub_domain = sub_domain
        elif cred_file:
            f = open(cred_file)
            credentials = json.loads(f.read())
            self.api_key = credentials['api_key']
            self.sub_domain = credentials['sub_domain']
        else:
            print("Need either an api_key and subdomain, or credential file. Exiting.")
            exit()

    def customer(self, nodename=''):
        return Customer(self.api_key, self.sub_domain, nodename)

    def product(self, nodename=''):
        return Product(self.api_key, self.sub_domain, nodename)

    def subscription(self, nodename=''):
        return Subscription(self.api_key, self.sub_domain, nodename)

    def credit_card(self, nodename=''):
        return CreditCard(self.api_key, self.sub_domain, nodename)

    def post_back(self, postbackdata):
        return PostBack(self.api_key, self.sub_domain, postbackdata)
