import ipaddress
import subprocess
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network


class HostScanner:

    @staticmethod
    def ping(target: IPv4Address | IPv6Address, count: int = 1) -> bool:
        """
        Check if a host is reachable (is up) using a ping
        command (subprocess).

        :param target: The IP address of the host to check.
        :param count: The number of ping packets to send. Default is 1.
        :return: Returns True if the host is reachable, otherwise False.
        """
        # ! this command doesn't work on Windows.
        command = ["ping", "-c", str(count), "-q", format(target)]
        try:
            # This approach is veeeeeeery slow
            result = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception as e:
            return False

    @staticmethod
    def ping_scan(
        network: IPv4Network | IPv6Network | str,
    ) -> list[IPv4Address | IPv6Address]:
        """
        Perform a ping scan on a network to identify reachable hosts.

        :param network: The network to scan, which can be a network object
                        or a string representing the network.
        :return: A list of IP addresses that are reachable in the specified network.
        """
        up_hosts = []

        if isinstance(network, str):
            target_network = ipaddress.ip_network(network)
        else:
            target_network = network

        for target_host in target_network.hosts():
            if HostScanner.ping(target_host):
                up_hosts.append(target_host)

        return up_hosts


if __name__ == "__main__":
    sc = HostScanner()
    net = ipaddress.ip_network("192.168.0.0/24")
    print("[*] Scanning...")
    hosts = sc.ping_scan(net)
    if len(hosts) > 1:
        print("[*] Hosts found: ")
        for i, host in enumerate(hosts):
            print(f"[{i}] {format(host)}")
