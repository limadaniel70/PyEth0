import platform

COMMON_TCP_PORTS: dict[int, str] = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    38: "rap",
    53: "dns",
    69: "tftp",
    80: "http",
    110: "pop3",
    123: "ntp",
    137: "netbios-ns",
    138: "netbios-dgm",
    139: "netbios-ssn",
    143: "imap",
    161: "snmp",
    179: "bgp",
    194: "irc",
    443: "https",
    465: "smtps",
    514: "syslog",
    515: "printer",
    993: "imaps",
    995: "pop3s",
    1080: "socks",
    1433: "ms-sql-s",
    1434: "ms-sql-m",
    1723: "pptp",
    3306: "mysql",
    3389: "rdp",
    5432: "postgresql",
    5900: "vnc",
    5984: "couchdb",
    6379: "redis",
    8080: "http-alt",
    8443: "https-alt",
    9000: "mongodb",
    11211: "memcached",
    27017: "mongodb",
}


def get_plataform() -> str:
    return platform.system()


PLATAFORM = get_plataform()
