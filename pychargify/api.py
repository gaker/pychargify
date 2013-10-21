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
import json
from pychargify import models


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

    # pylint: disable=W0232,R0903
    class Meta:
        url = 'customers.json'
        key = 'customer'
        required_fields = ('first_name', 'last_name', 'email', )
        read_only_fields = ('created_at', 'updated_at', 'id', )

    def __unicode__(self):
        return u'({0}) {1} {2}'.format(
            self.reference, self.first_name, self.last_name)

    def get_by_reference(self, reference):
        """
        Get a user by their reference name
        """
        self._meta.url = 'customers/lookup.json?reference={0}'.format(
            reference)
        content = self.get()
        # fix this
        self._meta.url = 'customers.json'
        return content

    # def get_subscriptions(self):
    #     obj = ChargifySubscription(self.api_key, self.sub_domain)
    #     return obj.getByCustomerId(self.id)


class Product(models.Model):
    """
    Represents Chargify Products
    """
    id = models.ChargifyField()
    price_in_cents = models.ChargifyField(value=0)
    name = models.ChargifyField()
    handle = models.ChargifyField()
    description = models.ChargifyField()
    product_family = models.ChargifyField(value={})
    accounting_code = models.ChargifyField()
    interval_unit = models.ChargifyField(value='day')  # month or day
    interval = models.ChargifyField(value=30)
    initial_charge_in_cents = models.ChargifyField(value=0)
    trial_price_in_cents = models.ChargifyField(value=0)
    trial_interval = models.ChargifyField(value=0)
    trial_interval_unit = models.ChargifyField(value='day')  # month or day
    expiration_interval = models.ChargifyField(value=0)
    expiration_interval_unit = models.ChargifyField(value='day')  # m or day
    return_url = models.ChargifyField(value='')
    require_credit_card = models.ChargifyField(value=True)
    created_at = models.ChargifyDateField()
    updated_at = models.ChargifyDateField()
    archived_at = models.ChargifyDateField()

    # pylint: disable=W0232,R0903
    class Meta:
        url = 'products.json'
        key = 'product'
        required_fields = ()
        read_only_fields = ('id', )

    def __unicode__(self):
        return self.name


# class Usage(object):
#     def __init__(self, id, memo, quantity):
#         self.id = id
#         self.quantity = int(quantity)
#         self.memo = memo


class Subscription(models.Model):
    """
    Represents Chargify Subscriptions
    """
    id = models.ChargifyField()
    activated_at = models.ChargifyDateField()
    created_at = models.ChargifyDateField()
    balance_in_cents = models.ChargifyField()
    cancel_at_end_of_period = models.ChargifyField()
    canceled_at = models.ChargifyField()
    cancellation_message = models.ChargifyField()
    coupon_code = models.ChargifyField()
    credit_card = models.ChargifyField()
    current_period_ends_at = models.ChargifyDateField()
    current_period_started_at = models.ChargifyDateField()
    customer = models.ChargifyField()
    delayed_cancel_at = models.ChargifyDateField()
    expires_at = models.ChargifyDateField()
    next_assessment_at = models.ChargifyDateField()
    payment_collection_method = models.ChargifyField()
    previous_state = models.ChargifyField()
    product = models.ChargifyField()
    signup_payment_id = models.ChargifyField()
    signup_revenue = models.ChargifyField()
    state = models.ChargifyField()
    total_revenue_in_cents = models.ChargifyField()
    trial_ended_at = models.ChargifyDateField()
    trial_started_at = models.ChargifyDateField()
    updated_at = models.ChargifyDateField()

    # pylint: disable=W0232,R0903
    class Meta:
        url = 'subscriptions.json'
        key = 'subscription'
        attribute_types = {
            'customer': 'Customer',
            'product': 'Product',
            # 'credit_card': 'ChargifyCreditCard'
        }

    def __unicode__(self):
        # pylint: disable=E1101
        return u'{0}-{1}'.format(
            self.product.__unicode__(), self.customer.__unicode__())

    def get(self, object_id=None, customer_id=None):
        """
        Subscriptions can be fetched by subscription or customer id.
        """
        if not customer_id:
            return super(Subscription, self).get(object_id=object_id)

        url = 'customers/{0}/subscriptions.json'.format(customer_id)
        content = self._get(url)
        return self.process_result(content)

    def get_statements(self, object_id=None, get_list=False):
        if object_id:
            if not get_list:
                url = 'subscriptions/{0}/statements.json'.format(object_id)
            else:
                url = 'subscriptions/{0}/statements/ids.json'.format(object_id)
        else:
            url = 'statements/ids.json'
        return self._get(url)

    def get_statement(self, object_id, get_pdf=False):
        url = 'statements/{0}.json'.format(object_id)
        headers = {}
        if get_pdf:
            url = 'statements/{0}.pdf'.format(object_id)
            headers.update({'Accept/Content-Type': 'application/pdf'})

        return self._get(url, **headers)


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


# class PostBack(models.Model):
#     """
#     Represents Chargify API Post Backs
#     """
#     subscriptions = []

#     def __init__(self, apikey, subdomain, postback_data):
#         super(PostBack, self).__init__(apikey, subdomain)
#         if postback_data:
#             self._process_postback_data(postback_data)

#     def _process_postback_data(self, data):
#         """
#         Process the Json array and fetches the Subscription Objects
#         """
#         csub = ChargifySubscription(self.api_key, self.sub_domain)
#         postdata_objects = json.loads(data)
#         for obj in postdata_objects:
#             self.subscriptions.append(csub.getBySubscriptionId(obj))


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
            file_ = open(cred_file)
            credentials = json.loads(file_.read())
            self.api_key = credentials['api_key']
            self.sub_domain = credentials['sub_domain']
        else:
            print("Need either an api_key and subdomain, "
                  "or credential file. Exiting.")
            exit()

    def customer(self, nodename=''):
        """
        Shortcut method to get the ``Customer`` object
        """
        return Customer(self.api_key, self.sub_domain, nodename)

    def product(self, nodename=''):
        """
        Shortcut method to get the ``Product`` object
        """
        return Product(self.api_key, self.sub_domain, nodename)

    def subscription(self, nodename=''):
        """
        Shortcut method to get the ``Subscription`` object
        """
        return Subscription(self.api_key, self.sub_domain, nodename)

    # def credit_card(self, nodename=''):
    #     """
    #     Shortcut method to get the ``CreditCard`` object
    #     """
    #     return CreditCard(self.api_key, self.sub_domain, nodename)

    # def post_back(self, postbackdata):
    #     """
    #     Shortcut method to get the ``PostBack`` object
    #     """
    #     return PostBack(self.api_key, self.sub_domain, postbackdata)
