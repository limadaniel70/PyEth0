import asyncio
import ipaddress
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

from pyeth0.constants import PLATFORM


class HostScanner:

    def __init__(self, network: IPv4Network | IPv6Network | str):
        self.target_network = HostScanner.resolve_network(network)
        self.n_of_hosts = self.target_network.num_addresses

    def change_network(self, new_network: IPv4Network | IPv6Network | str):
        """
        Updates the target network for the host scanner.

        Args:
            new_network (IPv4Network | IPv6Network | str): The new network to set, 
            which can be an IPv4 network, IPv6 network, or a string representation 
            of the network.
        """
        self.target_network = HostScanner.resolve_network(new_network)
        self.n_of_hosts = self.target_network.num_addresses

    @property
    def target_hosts(self) -> list[IPv6Address | IPv4Address]:
        """
        Generates a list containing the available hosts on a network.

        Returns:
            list[IPv6Address | IPv4Address]: List of available IPv6 
            or IPv4 addresses on the network.
        """
        return list(self.target_network.hosts())

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
    async def ping(target: IPv4Address | IPv6Address, count: int = 1) -> bool:
        """
        Check if a host is reachable (is up) using a ping
        command (subprocess).

        :param target: The IP address of the host to check.
        :param count: The number of ping packets to send. Default is 1.
        :return: Returns True if the host is reachable, otherwise False.
        """
        if PLATFORM == "Windows":
            command = ["ping", "/n", str(count), "/q", format(target)]
        else:
            command = ["ping", "-c", str(count), "-q", format(target)]

        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await process.communicate()
            return process.returncode == 0
        except Exception:
            return False

    async def ping_scan(self) -> list[IPv4Address | IPv6Address]:
        """
        Perform a ping scan on a network to identify reachable hosts.

        :return: A list of IP addresses that are reachable in the specified network.
        """
        tasks = [
            asyncio.create_task(self.ping(host)) for host in self.target_network.hosts()
        ]
        results = await asyncio.gather(*tasks)

        up_hosts = [
            host for host, is_up in zip(self.target_network.hosts(), results) if is_up
        ]
        return up_hosts
