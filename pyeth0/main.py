import socket
from ipaddress import ip_address

from constants import *

from pyeth0.port_scanner import PortScanner

host_name = "google.com"
host_ip = ip_address(socket.gethostbyname(host_name))
ports = PortScanner.scan_specific_ports(host_ip, [80, 443, 22, 20])

print(f"Open ports for {host_name} ({host_ip})")
for port in ports:
    print(f"PORT: {port} SERVICE: {COMMON_TCP_PORTS.get(port, 'Unknown')}")
