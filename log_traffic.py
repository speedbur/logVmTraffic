import os

from Database import Database
from XenTopOutputParser import XenTopOutputParser


def main():
    parser = XenTopOutputParser()
    data = parser.run()

    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "logvmtraffic.db")
    database = Database(path)
    for domain in data:
        database.store_domain_entry(domain)

if __name__ == "__main__":
    main()