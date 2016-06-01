import os

import settings
from Database import Database
from XenTopOutputParser import XenTopOutputParser


def main():
    parser = XenTopOutputParser()
    data = parser.run()

    database = Database(settings.DATABASE_PATH)
    for domain in data:
        database.store_domain_entry(domain)

if __name__ == "__main__":
    main()