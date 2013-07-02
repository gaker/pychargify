Chargify API wrapper for Python
===============================

pychargify
----------

This is a Python wrapper for the `Chargify <http://chargify.com>`_ API. 
It allows you to interface with the Chargify API using a simple object 
orientated syntax.


Add customer
++++++++++++

::

    chargify = Chargify('YOUR-API-KEY', 'YOUR-SUB-DOMAIN')

    customer = chargify.Customer()
    customer.first_name = 'John'
    customer.last_name = 'Doe'
    customer.email = 'john@doe.com'
    customer.save()

Create a subscription
+++++++++++++++++++++

::

    customer = chargify.Customer('customer_attributes')
    customer.first_name = 'Paul'
    customer.last_name = 'Trippett'
    customer.email = 'paul@getyouridx.com'

    creditcard = chargify.CreditCard('credit_card_attributes')
    creditcard.full_number = 1
    creditcard.expiration_month = 10
    creditcard.expiration_year = 2020

    subscription = chargify.Subscription()
    subscription.product_handle = 'fhaar-mini'
    subscription.customer = customer
    subscription.credit_card = creditcard

    subscription.save()

See tests.py for more usage examples.


Installation
------------

Place this library in your project and import the module

    from pychargify.api import *


Requirements
------------

* requests
* dateutil

Usage
-----

Documentation is in RestructuredText format in the docs directory.

Contributors
------------

* Paul Trippett (pyhub)  - Base Development
* mrtron - Several Updates and bug fixes to pychargify library
* Greg Aker (gaker) - Fork and rework (2013)
