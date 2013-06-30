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

import base64
import datetime
import json
import requests
import dateutil.parser
from itertools import chain

from pychargify import get_version
from .exceptions import (
    ChargifyError, ChargifyUnAuthorized,
    ChargifyForbidden, ChargifyNotFound,
    ChargifyUnProcessableEntity, ChargifyServerError
)


class ChargifyBase(object):
    """
    The ChargifyBase class provides a common base for all classes
    in this module
    @license    GNU General Public License
    """
    __ignore__ = ['api_key', 'sub_domain', 'base_host', 'request_host',
        'id', '__xmlnodename__']

    api_key = ''
    sub_domain = ''
    base_host = '.chargify.com'
    request_host = ''
    id = None

    def __init__(self, apikey, subdomain):
        """
        Initialize the Class with the API Key and SubDomain for Requests
        to the Chargify API
        """
        self.api_key = apikey
        self.sub_domain = subdomain
        self.request_host = "https://{0}{1}".format(
            self.sub_domain,
            self.base_host
        )

    def __get_xml_value(self, nodelist):
        """
        Get the Text Value from an XML Node
        """
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    def parse_fields(self, json_obj, obj_type):
        """
        Parse fields from a JSON response into an object.
        """
        constructor = globals()[self.__name__]
        obj = constructor(self.api_key, self.sub_domain)

        for field in self.__fields__:
            if field in self.__date_fields__:
                setattr(
                    obj, field,
                    dateutil.parser.parse(json_obj.get(obj_type, {}).get(field)))
            else:
                setattr(obj, field, json_obj.get(obj_type, {}).get(field))

        return obj

    def __get_object_from_node(self, json_obj, obj_type=''):
        """
        Copy values from a node into a new Object
        """
        import ipdb; ipdb.set_trace()
        if obj_type == '':
            constructor = globals()[self.__name__]
        else:
            constructor = globals()[obj_type]
        obj = constructor(self.api_key, self.sub_domain)

        # for k, v in json_obj.iteritems():
            # if childnodes.nodeType == 1 and not childnodes.nodeName == '':
            #     if childnodes.nodeName in self.__attribute_types__:
            #         obj.__setattr__(childnodes.nodeName,
            #             self._applyS(childnodes.toxml(),
            #             self.__attribute_types__[childnodes.nodeName],
            #                 childnodes.nodeName))
            #     else:
            #         node_value = self.__get_xml_value(childnodes.childNodes)
            #         if "type" in  childnodes.attributes.keys():
            #             node_type = childnodes.attributes["type"]
            #             if node_value:
            #                 if node_type.nodeValue == 'datetime':
            #                     node_value = datetime.datetime.fromtimestamp(
            #                         iso8601.parse(node_value))
            #         obj.__setattr__(childnodes.nodeName, node_value)
        return obj

    def fix_xml_encoding(self, xml):
        """
        Chargify encodes non-ascii characters in CP1252.
        Decodes and re-encodes with xml characters.
        Strips out whitespace "text nodes".
        """
        return unicode(''.join([i.strip() for i in xml.split('\n')])).encode(
            'CP1252', 'replace').decode('utf-8', 'ignore').encode(
            'ascii', 'xmlcharrefreplace')

    def _applyS(self, xml, obj_type, node_name):
        """
        Apply the values of the passed xml data to the a class
        """
        dom = minidom.parseString(self.fix_xml_encoding(xml))
        nodes = dom.getElementsByTagName(node_name)
        if nodes.length == 1:
            return self.__get_object_from_node(nodes[0], obj_type)

    def _applyA(self, resp, obj_type, node_name):
        """
        Apply the values of the passed data to a new class of the current type
        """
        objs = []
        import ipdb; ipdb.set_trace()
        for node in json.loads(resp):
            objs.append(self.__get_object_from_node(
                node[node_name], obj_type))
        return objs

    # def _toxml(self, dom):
    #     """
    #     Return a XML Representation of the object
    #     """
    #     element = minidom.Element(self.__xmlnodename__)
    #     for property, value in self.__dict__.iteritems():
    #         if not property in self.__ignore__:
    #             if property in self.__attribute_types__:
    #                 element.appendChild(value._toxml(dom))
    #             else:
    #                 node = minidom.Element(property)
    #                 node_txt = dom.createTextNode(str(value))
    #                 node.appendChild(node_txt)
    #                 element.appendChild(node)
    #     return element

    @property
    def headers(self):
        return {
            'user-agent': "pyChargify/{0}".format(get_version()),
            'content-type': 'application/json'
        }

    def check_response_code(self, status_code):

        # Unauthorized Error
        if status_code == 401:
            raise ChargifyUnAuthorized()

        # Forbidden Error
        elif status_code == 403:
            raise ChargifyForbidden()

        # Not Found Error
        elif status_code == 404:
            raise ChargifyNotFound()

        # Unprocessable Entity Error
        elif status_code == 422:
            raise ChargifyUnProcessableEntity()

        # Generic Server Errors
        elif status_code in [405, 500]:
            raise ChargifyServerError()

    def _get(self, url):
        """
        Handle HTTP GET's to the API
        """
        response = requests.get(
            "{0}/{1}".format(self.request_host, url.lstrip('/')),
            auth=(self.api_key, 'x'),
            headers=self.headers)

        self.check_response_code(response.status_code)

        return json.loads(response.content)

    def _post(self, url, data):
        """
        Handle HTTP POST's to the API
        """
        return self._request('POST', url, data)

    def _put(self, url, payload):
        """
        Handle HTTP PUT's to the API
        """
        response = requests.put(
            "{0}/{1}".format(self.request_host, url.lstrip('/')),
            auth=(self.api_key, 'x'),
            headers=self.headers,
            data=json.dumps(payload)
        )

        self.check_response_code(response.status_code)
        return json.loads(response.content)

    def _delete(self, url, data):
        """
        Handle HTTP DELETE's to the API
        """
        return self._request('DELETE', url, data)

    def _save(self, url, node_name):
        """
        Save the object using the passed URL as the API end point
        """
        obj_dict = {}

        for item in self.__fields__:
            if item not in ('id', 'created_at', 'updated_at'):
                obj_dict[item] = getattr(self, item)

        payload = {node_name: obj_dict}

        if self.id:
            return self._put(url, payload)
        else:
            obj = self._post()

        # dom = minidom.Document()
        # dom.appendChild(self._toxml(dom))

        # request_made = {
        #     'day': datetime.datetime.today().day,
        #     'month': datetime.datetime.today().month,
        #     'year': datetime.datetime.today().year
        # }

        # if self.id:
        #     obj = self._applyS(self._put('/' + url + '/' + self.id + '.xml',
        #         dom.toxml(encoding="utf-8")), self.__name__, node_name)
        #     if obj:
        #         if type(obj.updated_at) == datetime.datetime:
        #             if (obj.updated_at.day == request_made['day']) and \
        #                 (obj.updated_at.month == request_made['month']) and \
        #                 (obj.updated_at.year == request_made['year']):
        #                 self.saved = True
        #                 return (True, obj)
        #     return (False, obj)
        # else:
        #     obj = self._applyS(self._post('/' + url + '.xml',
        #         dom.toxml(encoding="utf-8")), self.__name__, node_name)
        #     if obj:
        #         if type(obj.updated_at) == datetime.datetime:
        #             if (obj.updated_at.day == request_made['day']) and \
        #                 (obj.updated_at.month == request_made['month']) and \
        #                 (obj.updated_at.year == request_made['year']):
        #                 return (True, obj)
        #     return (False, obj)

    def _get_auth_string(self):
        return base64.encodestring('%s:%s' % (self.api_key, 'x'))[:-1]

    def _request(self, method, url, data=''):
        """
        Handled the request and sends it to the server
        """
        http = httplib.HTTPSConnection(self.request_host)

        http.putrequest(method, url)
        http.putheader("Authorization", "Basic %s" % self._get_auth_string())
        http.putheader("User-Agent", "pychargify")
        http.putheader("Host", self.request_host)
        http.putheader("Accept", "application/xml")
        http.putheader("Content-Length", str(len(data)))
        http.putheader("Content-Type", 'text/xml; charset="UTF-8"')
        http.endheaders()

        print('sending: %s' % data)

        http.send(data)
        response = http.getresponse()

        # Unauthorized Error
        if response.status == 401:
            raise ChargifyUnAuthorized()

        # Forbidden Error
        elif response.status == 403:
            raise ChargifyForbidden()

        # Not Found Error
        elif response.status == 404:
            raise ChargifyNotFound()

        # Unprocessable Entity Error
        elif response.status == 422:
            raise ChargifyUnProcessableEntity()

        # Generic Server Errors
        elif response.status in [405, 500]:
            raise ChargifyServerError()

        return response.read()


class ChargifyCustomer(ChargifyBase):
    """
    Represents Chargify Customers
    @license    GNU General Public License
    """
    __name__ = 'ChargifyCustomer'
    __attribute_types__ = {}
    __fields__ = [
        'id', 'first_name', 'last_name', 'email',
        'city', 'address', 'address_2', 'state', 'zip',
        'country', 'phone', 'organization', 'reference',
        'created_at', 'updated_at', ]

    __date_fields__ = ['created_at', 'updated_at', ]

    id = None
    first_name = None
    last_name = None
    email = None
    city = None
    address = None
    address_2 = None
    state = None
    zip = None
    country = None
    phone = None
    organization = None
    reference = None
    created_at = None
    updated_at = None

    def __repr__(self):
        return '<ChargifyCustomer {0} {1}>'.format(self.first_name, self.last_name)

    def get(self, id=None):
        """
        Get a list of customers, or a customer by their internal id.
        """
        if not id:
            customers = self._get('customers.json')

            customer_list = set()
            for customer in customers:
                customer_list.add(self.parse_fields(customer, 'customer'))
            return list(customer_list)

        customer = self._get('customers/{0}.json'.format(str(id)))
        return self.parse_fields(customer, 'customer')

    def get_by_reference(self, reference):
        customer = self._get(
            'customers/lookup.json?reference={0}'.format(reference)
        )
        return self.parse_fields(customer, 'customer')

    # def get_subscriptions(self):
    #     obj = ChargifySubscription(self.api_key, self.sub_domain)
    #     return obj.getByCustomerId(self.id)

    def save(self):
        if self.id:
            url = 'customers/{0}.json'.format(self.id)
        else:
            url = 'customers.json'
        customer = self._save(url, 'customer')
        return self.parse_fields(customer, 'customer')


class ChargifyProduct(ChargifyBase):
    """
    Represents Chargify Products
    @license    GNU General Public License
    """
    __name__ = 'ChargifyProduct'
    __attribute_types__ = {}
    __xmlnodename__ = 'product'

    id = None
    price_in_cents = 0
    name = ''
    handle = ''
    product_family = {}
    accounting_code = ''
    interval_unit = ''
    interval = 0

    def __init__(self, apikey, subdomain, nodename=''):
        super(ChargifyProduct, self).__init__(apikey, subdomain)
        if nodename:
            self.__xmlnodename__ = nodename

    def getAll(self):
        return self._applyA(self._get('/products.xml'),
            self.__name__, 'product')

    def getById(self, id):
        return self._applyS(self._get('/products/' + str(id) + '.xml'),
            self.__name__, 'product')

    def getByHandle(self, handle):
        return self._applyS(self._get('/products/handle/' + str(handle) +
            '.xml'), self.__name__, 'product')

    def save(self):
        return self._save('products', 'product')

    def getPaymentPageUrl(self):
        return ('https://' + self.request_host + '/h/' +
            self.id + '/subscriptions/new')

    def getPriceInDollars(self):
        return round(float(self.price_in_cents) / 100, 2)

    def getFormattedPrice(self):
        return "$%.2f" % (self.getPriceInDollars())


class Usage(object):
    def __init__(self, id, memo, quantity):
        self.id = id
        self.quantity = int(quantity)
        self.memo = memo


class ChargifySubscription(ChargifyBase):
    """
    Represents Chargify Subscriptions
    @license    GNU General Public License
    """
    __name__ = 'ChargifySubscription'
    __attribute_types__ = {
        'customer': 'ChargifyCustomer',
        'product': 'ChargifyProduct',
        'credit_card': 'ChargifyCreditCard'
    }
    __xmlnodename__ = 'subscription'

    id = None
    state = ''
    balance_in_cents = 0
    current_period_started_at = None
    current_period_ends_at = None
    trial_started_at = None
    trial_ended_attrial_ended_at = None
    activated_at = None
    expires_at = None
    created_at = None
    updated_at = None
    customer = None
    product = None
    product_handle = ''
    credit_card = None

    def __init__(self, apikey, subdomain, nodename=''):
        super(ChargifySubscription, self).__init__(apikey, subdomain)
        if nodename:
            self.__xmlnodename__ = nodename

    def getAll(self):
        return self._applyA(self._get('/subscriptions.xml'),
            self.__name__, 'subscription')

    def createUsage(self, component_id, quantity, memo=None):
        """
        Creates usage for the given component id.
        """

        data = '''<?xml version="1.0" encoding="UTF-8"?><usage>
            <quantity>%d</quantity><memo>%s</memo></usage>''' % (
                quantity, memo or "")

        dom = minidom.parseString(self.fix_xml_encoding(
            self._post('/subscriptions/%s/components/%d/usages.xml' % (
                str(self.id), component_id), data)))

        return [Usage(*tuple(chain.from_iterable([[x.data
            for x in i.childNodes] or [None] for i in n.childNodes])))
            for n in dom.getElementsByTagName('usage')]

    def getByCustomerId(self, customer_id):
        return self._applyA(self._get('/customers/' + str(customer_id) +
            '/subscriptions.xml'), self.__name__, 'subscription')

    def getBySubscriptionId(self, subscription_id):
        #Throws error if more than element is returned
        i, = self._applyA(self._get('/subscriptions/' + str(subscription_id) +
            '.xml'), self.__name__, 'subscription')
        return i

    def save(self):
        return self._save('subscriptions', 'subscription')

    def resetBalance(self):
        self._put("/subscriptions/" + self.id + "/reset_balance.xml", "")

    def reactivate(self):
        self._put("/subscriptions/" + self.id + "/reactivate.xml", "")

    def upgrade(self, toProductHandle):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
  <subscription>
    <product_handle>%s</product_handle>
  </subscription>""" % (toProductHandle)
        #end improper indentation

        return self._applyS(self._put("/subscriptions/" + self.id + ".xml",
            xml), self.__name__, "subscription")

    def unsubscribe(self, message):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<subscription>
  <cancellation_message>
    %s
  </cancellation_message>
</subscription>""" % (message)

        self._delete("/subscriptions/" + self.id + ".xml", xml)


class ChargifyCreditCard(ChargifyBase):
    """
    Represents Chargify Credit Cards
    """
    __name__ = 'ChargifyCreditCard'
    __attribute_types__ = {}
    __xmlnodename__ = 'credit_card_attributes'

    first_name = ''
    last_name = ''
    full_number = ''
    masked_card_number = ''
    expiration_month = ''
    expiration_year = ''
    cvv = ''
    type = ''
    billing_address = ''
    billing_city = ''
    billing_state = ''
    billing_zip = ''
    billing_country = ''
    zip = ''

    def __init__(self, apikey, subdomain, nodename=''):
        super(ChargifyCreditCard, self).__init__(apikey, subdomain)
        if nodename:
            self.__xmlnodename__ = nodename

    def save(self, subscription):
        path = "/subscriptions/%s.xml" % (subscription.id)

        data = u"""<?xml version="1.0" encoding="UTF-8"?>
  <subscription>
    <credit_card_attributes>
      <full_number>%s</full_number>
      <expiration_month>%s</expiration_month>
      <expiration_year>%s</expiration_year>
      <cvv>%s</cvv>
      <first_name>%s</first_name>
      <last_name>%s</last_name>
      <zip>%s</zip>
    </credit_card_attributes>
  </subscription>""" % (self.full_number, self.expiration_month,
          self.expiration_year, self.cvv, self.first_name,
          self.last_name, self.zip)
        # end improper indentation

        return self._applyS(self._put(path, data),
            self.__name__, "subscription")


class ChargifyPostBack(ChargifyBase):
    """
    Represents Chargify API Post Backs
    @license    GNU General Public License
    """
    subscriptions = []

    def __init__(self, apikey, subdomain, postback_data):
        ChargifyBase.__init__(apikey, subdomain)
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


class Chargify:
    """
    The Chargify class provides the main entry point to the Chargify API
    @license    GNU General Public License
    """
    api_key = ''
    sub_domain = ''

    def __init__(self, apikey=None, subdomain=None, cred_file=None):
        ''' We take either an api_key and sub_domain, or a path
        to a file with JSON that defines those two, or we throw
        an error.'''

        if self.api_key and self.sub_domain:
            self.api_key = apikey
            self.sub_domain = subdomain
            return
        elif cred_file:
            f = open(cred_file)
            credentials = json.loads(f.read())
            self.api_key = credentials['api_key']
            self.sub_domain = credentials['sub_domain']
            return
        else:
            print "Need either an api_key and subdomain, or credential file. Exiting."
            exit()

    def Customer(self, nodename=''):
        return ChargifyCustomer(self.api_key, self.sub_domain, nodename)

    def Product(self, nodename=''):
        return ChargifyProduct(self.api_key, self.sub_domain, nodename)

    def Subscription(self, nodename=''):
        return ChargifySubscription(self.api_key, self.sub_domain, nodename)

    def CreditCard(self, nodename=''):
        return ChargifyCreditCard(self.api_key, self.sub_domain, nodename)

    def PostBack(self, postbackdata):
        return ChargifyPostBack(self.api_key, self.sub_domain, postbackdata)
