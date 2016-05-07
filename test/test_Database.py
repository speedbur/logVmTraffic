import os
import unittest

from Database import Database
from DomainLogEntry import DomainLogEntry
from XenTopOutputParser import XenTopOutputParser


class DatabaseTest(unittest.TestCase):


    def test_create_tables(self):
        self.database = Database("/tmp/lala.db")
        os.unlink("/tmp/lala.db")

    def test_store_domain_entry(self):
        self.database = Database("/tmp/lala.db")

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
