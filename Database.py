import os
import time

try:
    import sqlite
except:
    import sqlite3 as sqlite


class Database(object):

    def __init__(self, filename):
        create_database = not os.path.exists(filename)
        self._connection = sqlite.connect(filename)
        if create_database:
            self._create_database_structure()

    def _create_database_structure(self):
        cursor = self._connection.cursor()
        cursor.execute("""
            CREATE TABLE domain (
                id     INTEGER   PRIMARY KEY AUTOINCREMENT,
                name   TEXT      NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE logentry (
                id             INTEGER   PRIMARY KEY AUTOINCREMENT,
                domain_id      INTEGER NOT NULL,
                timestamp      INTEGER NOT NULL,
                cpu_seconds    INTEGER NOT NULL,
                memory         INTEGER NOT NULL,
                memory_percent FLOAT NOT NULL,
                max_memory     INTEGER NOT NULL,
                max_memory_percent FLOAT NOT NULL,
                virtual_cpus   INTEGER NOT NULL,

                FOREIGN KEY(domain_id) REFERENCES domain(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE networkentry (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                logentry_id     INTEGER NOT NULL,
                interface       TEXT NOT NULL,
                rx_bytes        INTEGER NOT NULL,
                rx_packets      INTEGER NOT NULL,
                rx_error        INTEGER NOT NULL,
                rx_drop         INTEGER NOT NULL,
                tx_bytes        INTEGER NOT NULL,
                tx_packets      INTEGER NOT NULL,
                tx_error        INTEGER NOT NULL,
                tx_drop         INTEGER NOT NULL,

                FOREIGN KEY(logentry_id) REFERENCES logentry(id)
            )
        """)
        self._connection.commit()

    def store_domain_entry(self, domain):
        """
        stores a domain entry to the database
        :param domain: a DomainLogEntry instance
        """
        # fetch domain id and store a new domain if the name was unknown
        cursor = self._connection.cursor()
        cursor.execute("select id from domain where name=%s", (domain.name,))
        element = cursor.fetchone()

        if element is not None:
            domain_id = element[0]
        else:
            cursor.execute("insert into domain (name) VALUES (%s)", (domain.name, ))
            domain_id = cursor.lastrowid

        # log the main data
        unix_timestamp = int(time.time())

        cursor.execute("insert into logentry (domain_id, timestamp, cpu_seconds, memory, memory_percent, max_memory, max_memory_percent, virtual_cpus) VALUES (%d, %d, %d, %d, %2.2f, %d, %2.2f, %d)",
                       (domain_id, unix_timestamp, domain.cpu_seconds, domain.memory, domain.memory_percent, domain.max_memory, domain.max_memory_percent, domain.virtual_cpus))
        entry_id = cursor.lastrowid

        # log network data
        for network in domain.networks:
            cursor.execute("insert into networkentry (logentry_id, interface, rx_bytes, rx_packets, rx_error, rx_drop, tx_bytes, tx_packets, tx_error, tx_drop) VALUES (%d, %s, %d, %d, %d, %d, %d, %d, %d, %d)",
                           (entry_id, network.name, network.rx.bytes, network.rx.packets, network.rx.packets, network.rx.error, network.tx.bytes, network.tx.packets, network.tx.packets, network.tx.error))

        self._connection.commit()
