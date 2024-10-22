#  Copyright (c) 2024 Daniel Lima
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import socket
from ipaddress import IPv4Address, IPv6Address, ip_address


class PortScanner:

    @staticmethod
    def scan_specific_ports(
            target: IPv4Address | IPv6Address | str, ports: list[int]
    ) -> list[int]:
        """
        Scans the target host for open ports from a specific list.

        Args:
            target (ip_address | str): Target IP address or hostname.
            ports (list[int]): List of ports to scan.

        Returns:
            list[int]: List of open ports.
        """
        open_ports: list[int] = []

        if isinstance(target, str):
            target_host = ip_address(socket.gethostbyname(target))
        else:
            target_host = target

        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Set timeout for the connection attempt
                result = s.connect_ex((str(target_host), port))
                if result == 0:
                    open_ports.append(port)

        return open_ports

    @staticmethod
    def scan_port(target: IPv4Address | IPv6Address | str, port: int) -> bool:
        """
        Checks if a specific port is open on the target host.

        Args:
            target (ip_address | str): Target IP address or hostname.
            port (int): Port to check.

        Returns:
            bool: True if the port is open, False otherwise.
        """
        if isinstance(target, str):
            target_host = ip_address(socket.gethostbyname(target))
        else:
            target_host = target

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((str(target_host), port)) == 0

    @staticmethod
    def get_open_ports(
            target: IPv4Address | IPv6Address | str,
            port_range: tuple[int, int] = (0, 65535),
    ) -> list[int]:
        """
        Scans the target host for open ports within the given range.

        Args:
            target (ip_address | str): Target IP address or hostname.
            port_range (tuple[int, int], optional): Range of ports to scan. Defaults to (0, 65535).

        Returns:
            list[int]: List of open ports.
        """
        open_ports: list[int] = []

        if isinstance(target, str):
            target_host = ip_address(socket.gethostbyname(target))
        else:
            target_host = target

        for port in range(port_range[0], port_range[1]):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((str(target_host), port))
                if result == 0:
                    open_ports.append(port)
        return open_ports
