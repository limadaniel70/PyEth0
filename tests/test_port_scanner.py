from pyeth0.port_scanner import PortScanner
from ipaddress import ip_address


class TestPortScanner:

    def test_scan_port_open(self):
        target = "scanme.nmap.org"
        port = 22
        assert PortScanner.scan_port(target, port) == True

    def test_scan_port_closed(self):
        target = "scanme.nmap.org"
        port = 9999
        assert PortScanner.scan_port(target, port) == False

    def test_scan_specific_ports(self):
        target = "localhost"
        ports_to_scan = [80, 22, 9999]
        open_ports = PortScanner.scan_specific_ports(target, ports_to_scan)
        assert all(port in ports_to_scan for port in open_ports)

    def test_get_open_ports(self):
        target = "localhost"
        port_range = (80, 90)
        open_ports = PortScanner.get_open_ports(target, port_range)
        assert all(
            port in range(port_range[0], port_range[1] + 1) for port in open_ports
        )
