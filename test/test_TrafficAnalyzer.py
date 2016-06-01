import os
import unittest

from Database import Database
from TrafficAnalyzer import TrafficAnalyzer


class TrafficAnalyzerTest(unittest.TestCase):

    def setUp(self):
        super(TrafficAnalyzerTest, self).setUp()
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "testdata.db")
        database = Database(path)
        self.analyzer = TrafficAnalyzer(database)

    def test_analyze_for_domain_and_time_range_monthly(self):
        result = self.analyzer.analyze_for_domain_and_time_range_monthly(7, 0, 99999999999999)
        pass