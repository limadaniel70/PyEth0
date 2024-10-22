import ipaddress
import subprocess


class Scan:

    @staticmethod
    def ping(host: ipaddress.ip_address, count: int = 1) -> bool:
        command = ["ping", "-c", str(count), "-q", format(host)]
        try:
            result = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception as e:
            return False

    def ping_scan(self, network: ipaddress.ip_network) -> list[ipaddress.IPv4Address]:
        up_hosts = []
        for host in network.hosts():
            if self.ping(host):
                up_hosts.append(host)
        return up_hosts


if __name__ == "__main__":
    sc = Scan()
    net = ipaddress.ip_network("192.168.0.0/24")
    print("[*] Scanning...")
    hosts = sc.ping_scan(net)
    if len(hosts) > 1:
        print("[*] Hosts found: ")
        for i, host in enumerate(hosts):
            print(f"[{i}] {format(host)}")
