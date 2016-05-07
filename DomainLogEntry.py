
class NetworkInfoEntry(object):
    def __init__(self):
        self.bytes = 0
        self.packets = 0
        self.error = 0
        self.drop = 0


class NetworkLogEntry(object):
    def __init__(self):
        self.name = ""
        self.rx = NetworkInfoEntry()
        self.tx = NetworkInfoEntry()


class DomainLogEntry(object):
    def __init__(self):
        self.name =  ""
        self.cpu_seconds = 0
        self.memory = 0
        self.memory_percent = 0.0
        self.max_memory = 0
        self.max_memory_percent = 0.0
        self.virtual_cpus = 0
        self.networks = []

    def __str__(self):
        result = self.name
        for network in self.networks:
            result += ", " + network.name + " (RX:" + str(network.rx.bytes/1024/1024/1024) +"gb, TX:" + str(network.tx.bytes/1024/1024/1024) + "gb)"
        return result
