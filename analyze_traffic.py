import os

import settings
from Database import Database
from TrafficAnalyzer import TrafficAnalyzer


def main():
    database = Database(settings.DATABASE_PATH)
    domain_list = database.get_all_domains()
    analyzer = TrafficAnalyzer(database)
    for domain in domain_list:
        print domain[1]
        result = analyzer.analyze_for_domain_and_time_range_monthly(domain[0], 0, 9999999999)
        for item in result:
            print item["date"] + " " + item["interface"] + " " + str(item["rx_bytes"] / 1024 / 1024 / 1024) + "gb " + str(item["tx_bytes"] / 1024 / 1024 / 1024) + "gb"
        print


if __name__ == "__main__":
    main()