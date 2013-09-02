"""
Base test file.
"""

import json
import os
import unittest


class TestBase(unittest.TestCase):

    def load_fixtures(self, filename):

        fixtures_dir = os.path.join(
            os.path.dirname(__file__),
            'fixtures'
        )

        fixtures_file = os.path.join(
            fixtures_dir, "{0}.json".format(filename)
        )

        if not os.path.exists(fixtures_file):
            raise Exception("Fixtures file not found.")

        with open(fixtures_file, 'r') as f:
            return json.loads(f.read())
