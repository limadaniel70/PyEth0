import ipaddress
import subprocess
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from math import floor, log2
from multiprocessing import pool

from pyeth0.constants import PLATAFORM


class HostScanner:

    def __init__(self, network: IPv4Network | IPv6Network | str):
        self.target_network = HostScanner.resolve_network(network)
        self.n_of_hosts = self.target_network.num_addresses

    def change_network(self, new_network: IPv4Network | IPv6Network | str):
        self.target_network = HostScanner.resolve_network(new_network)
        self.n_of_hosts = self.target_network.num_addresses

    @property
    def target_hosts(self) -> list[IPv6Address | IPv4Address]:
        return list(self.target_network.hosts())

    @staticmethod
    def calc_procs(n_of_hosts: int) -> int:
        return max(4, floor(log2(n_of_hosts))) * 2

    @staticmethod
    def resolve_network(
        network: IPv4Network | IPv6Network | str,
    ) -> IPv4Network | IPv6Network:
        """
        Resolves a network identifier to an IPv4 or IPv6 network object.

        :param network: The network to resolve, either as an IPv4/IPv6 network object or a string.
        :return: An IPv4Network or IPv6Network object representing the specified network.
        """
        if isinstance(network, str):
            return ipaddress.ip_network(network)
        return network

    @staticmethod
    def ping(target: IPv4Address | IPv6Address, count: int = 1) -> bool:
        """
        Check if a host is reachable (is up) using a ping
        command (subprocess).

        :param target: The IP address of the host to check.
        :param count: The number of ping packets to send. Default is 1.
        :return: Returns True if the host is reachable, otherwise False.
        """
        if PLATAFORM == "Windows":
            command = ["ping", "/n", str(count), "/q", format(target)]
        else:
            command = ["ping", "-c", str(count), "-q", format(target)]

        try:
            # This approach is veeeeeeery slow
            result = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception as e:
            return False

    def ping_scan(self) -> list[IPv4Address | IPv6Address]:
        """
        Perform a ping scan on a network to identify reachable hosts.

        :return: A list of IP addresses that are reachable in the specified network.
        """
        with pool.Pool(processes=HostScanner.calc_procs(self.n_of_hosts)) as p:
            result = p.map(self.ping, list(self.target_network.hosts()))

        up_hosts = [
            host for n, host in enumerate(self.target_network.hosts()) if result[n]
        ]
        return up_hosts


if __name__ == "__main__":
    sc = HostScanner("192.168.0.0/24")
    print("[*] Scanning...")
    hosts = sc.ping_scan()
    if len(hosts) > 1:
        print("[*] Hosts found: ")
        for i, host in enumerate(hosts):
            print(f"[{i}] {format(host)}")
