# noinspection PyMethodMayBeStatic
from datetime import datetime


class TrafficAnalyzer(object):

    def __init__(self, database):
        self.database = database

    def _get_datetime_from_unix_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp)

    def analyze_for_domain_and_time_range_monthly(self, domain_id, from_timestamp, to_timestamp):
        """
        analyzes the daily traffic for the given domain and time range
        :param domain_id: the id of the domain
        :param from_timestamp: the starting timestamp
        :param to_timestamp: the ending timestamp
        :return: TODO result stuff
        """
        data = self.database.fetch_network_data_for_domain_and_time_range(domain_id, from_timestamp, to_timestamp)
        if len(data) == 0:
            return []

        result = []
        current_network_interface = data[0]["interface"]
        current_counter = 0
        current_day = self._get_datetime_from_unix_timestamp(data[0]["timestamp"])
        rx_bytes = 0
        tx_bytes = 0
        old_rx_bytes = data[0]["rx_bytes"]
        old_tx_bytes = data[0]["tx_bytes"]
        for entry in data:
            entry_day = self._get_datetime_from_unix_timestamp(entry["timestamp"])
            if current_network_interface != entry["interface"] or current_day.month != entry_day.month:
                # next interface starts
                result.append({
                    "date": current_day.strftime("%Y-%m"),
                    "interface": current_network_interface,
                    "rx_bytes": rx_bytes,
                    "tx_bytes": tx_bytes
                })
                rx_bytes = 0
                tx_bytes = 0
                current_network_interface = entry["interface"]
                current_day = self._get_datetime_from_unix_timestamp(entry["timestamp"])
                old_rx_bytes = entry["rx_bytes"]
                old_tx_bytes = entry["tx_bytes"]

            if old_rx_bytes < entry["rx_bytes"]:
                rx_bytes += (entry["rx_bytes"] - old_rx_bytes)
                old_rx_bytes = entry["rx_bytes"]
            if old_tx_bytes < entry["tx_bytes"]:
                tx_bytes += (entry["tx_bytes"] - old_tx_bytes)
                old_tx_bytes = entry["tx_bytes"]

        result.append({
            "date": current_day.strftime("%Y-%m"),
            "interface": current_network_interface,
            "rx_bytes": rx_bytes,
            "tx_bytes": tx_bytes
        })
        return result
