import os
import unittest

from Database import Database
from DomainLogEntry import DomainLogEntry
from XenTopOutputParser import XenTopOutputParser


# noinspection PyMethodMayBeStatic
class DatabaseTest(unittest.TestCase):


    def test_create_tables(self):
        database = Database("/tmp/lala.db")
        os.unlink("/tmp/lala.db")

    def test_store_domain_entry(self):
        database = Database("/tmp/lala.db")

        domain = DomainLogEntry()
        domain.name = "Test"
        self.database.store_domain_entry(domain)
        domain.name = "Test 2"
        self.database.store_domain_entry(domain)
        domain.name = "Test"
        self.database.store_domain_entry(domain)

        os.unlink("/tmp/lala.db")

    def test_log_complete(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "testdata.txt")
        f = open(path, "r")
        try:
            data = f.read()
            domains = XenTopOutputParser()._parse_output(data)
            database = Database("/tmp/lala.db")
            for domain in domains:
                database.store_domain_entry(domain)
        finally:
            f.close()
        os.unlink("/tmp/lala.db")

    def test_fetch_all_domains(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "testdata.db")
        database = Database(path)
        result = database.get_all_domains()
        self.assertEquals(len(result), 14)

    def test_fetch_network_data_for_domain_and_time_range(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "testdata.db")
        database = Database(path)
        result = database.fetch_network_data_for_domain_and_time_range(7, 1462635336, 1463479263)
        self.assertEquals(len(result), 708)