import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import unittest
import re
import scre
from re_tests import tests, SUCCEED, FAIL, SYNTAX_ERROR
class TestStringMethods(unittest.TestCase):

    def test_re(self):
        for element in tests:
            try:
                obj = re.search(element[0], element[1])
                if obj is None:
                    status = FAIL
                else:
                    status = SUCCEED
            except:
                status = SYNTAX_ERROR
            self.assertEqual(status, element[2], element)
if __name__ == '__main__':
    unittest.main()