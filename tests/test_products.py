# """
# Test Product endpoints
# """
# import datetime
# import json

# from httpretty import HTTPretty, httprettified
# from nose.tools import raises

# from pychargify.api import Product
# from .base import TestBase


# class TestProducts(TestBase):

#     def setUp(self):
#         self.products_list = self.load_fixtures('products')

#     @httprettified
#     def test_get_product_list(self):
#         """
#         Test getting a list of products.
#         """
#         HTTPretty.register_uri(
#             HTTPretty.GET,
#             "https://some-test.chargify.com/products.json",
#             body=json.dumps(self.products_list))

#         obj = Product('1234', 'some-test')
#         products = obj.get()

#         self.assertTrue(len(products), 2)

#     @httprettified
#     def test_get_product(self):
#         """
#         Test getting a product
#         """
#         HTTPretty.register_uri(
#             HTTPretty.GET,
#             "https://some-test.chargify.com/products/2.json",
#             body=json.dumps(self.products_list[0]))

#         obj = Product('1234', 'some-test')
#         product = obj.get(id=2)

#         self.assertTrue(product.require_credit_card)
