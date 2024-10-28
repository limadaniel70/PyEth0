from ipaddress import IPv4Network, IPv4Address
from pyeth0.host_scanner import HostScanner

class TestHostScanner:

    async def test_ping_scan(self):
        target_network = IPv4Network("192.168.0.0/24")
        default_gateway = IPv4Address("192.168.0.1")
        hc = HostScanner(target_network)
        hosts = await hc.ping_scan()
        assert default_gateway in hosts