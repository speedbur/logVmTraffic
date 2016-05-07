import os
import unittest

from XenTopOutputParser import XenTopOutputParser


class XenTopOutputParserText(unittest.TestCase):


    def test_parse_output(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "testdata.txt")
        f = open(path, "r")
        try:
            data = f.read()
            domains = XenTopOutputParser()._parse_output(data)
        finally:
            f.close()

        print domains
