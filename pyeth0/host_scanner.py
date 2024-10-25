import ipaddress
import subprocess
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from multiprocessing import pool

from pyeth0.constants import PLATAFORM


class HostScanner:

    def __init__(self, network: IPv4Network | IPv6Network | str):
        self.target_network = HostScanner.resolve_network(network)
        self.n_of_hosts = self.target_network.num_addresses

    @staticmethod
    def resolve_network(
        network: IPv4Network | IPv6Network | str,
    ) -> IPv4Network | IPv6Network:
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
            command = ["ping", "-n", str(count), "-q", format(target)]
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

        target_hosts = list(self.target_network.hosts())

        with pool.Pool() as p:
            result = p.map(self.ping, target_hosts)

        up_hosts = [host for host, val in zip(target_hosts, result) if val == True]
        return up_hosts


if __name__ == "__main__":
    sc = HostScanner("192.168.0.0/24")
    print("[*] Scanning...")
    hosts = sc.ping_scan()
    if len(hosts) > 1:
        print("[*] Hosts found: ")
        for i, host in enumerate(hosts):
            print(f"[{i}] {format(host)}")
