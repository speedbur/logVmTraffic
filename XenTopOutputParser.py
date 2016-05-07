import os
import re

from DomainLogEntry import DomainLogEntry, NetworkLogEntry


class XenTopOutputParser(object):

    def __init__(self):
        self.command = "xentop -d 1 -b -i 3 -f -n "

        # regex for headerline matches:
        #'      NAME  STATE   CPU(sec) CPU(%)     MEM(k) MEM(%)  MAXMEM(k) MAXMEM(%) VCPUS NETS NETTX(k) NETRX(k) VBDS   VBD_OO   VBD_RD   VBD_WR  VBD_RSECT  VBD_WSECT SSID'
        self.header_regex = re.compile(ur'^\s*NAME\s+STATE+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s*$')

        # 'BB - backup2 --b---      11235    0.0    3145728    4.7    3145728       4.7     2    1 36203731 35046295    0        0        0        0          0          0    0'
        self.domain_line_regex = re.compile(ur'^(?P<name>.+)\s+(?P<state>[a-zA-Z-]{6})\s+(?P<cpu_seconds>\d+)\s+\d+\.\d+\s+(?P<mem>\d+)\s+(?P<mem_percent>\d+\.\d+)\s+(?P<max_mem>\d+)\s+(?P<max_mem_percent>\d+\.\d+)\s+(?P<vcpus>\d+)\s+(?P<nets>\d+)\s+(?P<net_domain_tx>\d+)\s+(?P<net_domain_rx>\d+).*$')

        # 'Net0 RX: 482159350480bytes 484063974pkts        0err        0drop  TX: 107249393069bytes 342275714pkts        0err        0drop'
        self.network_line_regex = re.compile(ur'^(?P<network_name>Net\d+)\s+RX:\s+(?P<rx_bytes>\d+)bytes\s+(?P<rx_packets>\d+)pkts\s+(?P<rx_error>\d+)err\s+(?P<rx_drop>\d+)drop\s+TX:\s+(?P<tx_bytes>\d+)bytes\s+(?P<tx_packets>\d+)pkts\s+(?P<tx_error>\d+)err\s+(?P<tx_drop>\d+)drop.*$')

    def run(self):
        command_line_result = os.popen(self.command)
        data = ""
        for line in command_line_result:
            data += line + "\n"
        return self._parse_output(data)

    def _parse_output(self, complete_data):
        """
        parses the output of the xentop command
        :param complete_data: the complete data with network stuff only the third iteration is parsed, because
        network data is only present after the third iteration of the output
        :return: an array of Domain objects
        """
        result = []
        iteration_counter = 0
        current_domain = None
        for line in complete_data.split("\n"):
            if line == "":
                continue

            if iteration_counter < 3:
                # skip first two headers, because they contain no network info
                if re.match(self.header_regex, line) is not None:
                    iteration_counter += 1
            else:
                domain_match = re.match(self.domain_line_regex, line)
                if domain_match is not None:
                    current_domain = DomainLogEntry()
                    current_domain.name = domain_match.group("name")
                    current_domain.cpu_seconds = int(domain_match.group("cpu_seconds"))
                    current_domain.max_memory = int(domain_match.group("max_mem"))
                    current_domain.max_memory_percent = float(domain_match.group("max_mem_percent"))
                    current_domain.memory = int(domain_match.group("mem"))
                    current_domain.memory_percent = float(domain_match.group("mem_percent"))
                    current_domain.virtual_cpus = int(domain_match.group("vcpus"))
                    result.append(current_domain)
                else:
                    # network match
                    network_match = re.match(self.network_line_regex, line)
                    network = NetworkLogEntry()
                    network.name = network_match.group("network_name")
                    network.rx.bytes = int(network_match.group("rx_bytes"))
                    network.rx.packets = int(network_match.group("rx_packets"))
                    network.rx.error = int(network_match.group("rx_error"))
                    network.rx.drop = int(network_match.group("rx_drop"))
                    network.tx.bytes = int(network_match.group("tx_bytes"))
                    network.tx.packets = int(network_match.group("tx_packets"))
                    network.tx.error = int(network_match.group("tx_error"))
                    network.tx.drop = int(network_match.group("tx_drop"))
                    current_domain.networks.append(network)

        return result