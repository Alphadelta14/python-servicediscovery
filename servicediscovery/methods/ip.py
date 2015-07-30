
from servicediscovery.methods import Method


class IPAddress(object):
    """A comparable IP address handler"""
    def __init__(self, ip_address):
        self.octets = [int(ip_oct) for ip_oct in ip_address.split('.')]
        assert len(self.octets) == 4

    def __eq__(self, other):
        return self.octets == other.octets

    def __lt__(self, other):
        for octet_a, octet_b in zip(self.octets, other.octets):
            if octet_a < octet_b:
                return True
            elif octet_a > octet_b:
                return False
        return False

    def __le__(self, other):
        for octet_a, octet_b in zip(self.octets, other.octets):
            if octet_a < octet_b:
                return True
            elif octet_a > octet_b:
                return False
        return True

    def incr(self, amount=1):
        """Increases the current IP Address

        Parameters
        ----------
        amount : int, optional
            Amount to increase. Defaults to 1.

        Returns
        -------
        address : IPAddress
            self after the change
        """
        for octet_idx in range(4)[::-1]:
            self.octets[octet_idx] += int(amount)
            if self.octets[octet_idx] > 255:
                amount = self.octets[octet_idx]/256
                self.octets[octet_idx] -= 256
            else:
                amount = 0
        return self

    def __str__(self):
        return '.'.join(str(octet) for octet in self.octets)


class StaticIPMethod(Method):
    """Checks a static IP for the registry

    Attributes
    ----------
    ip_address : str
    port : int
    """
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def get_registry(self):
        """Checks the IP for the registry"""
        found_address, found_port = self.check_ip(self.ip_address, self.port)
        if found_address is None:
            return None
        return self.found_registry(found_address, found_port)


class ScanIPRangeMethod(Method):
    """Scans a range of IPs and ports for the registry.
    This is generally not recommended, as it can hit a lot of hosts.


    10.0.0.0 - 10.0.255.255 is 65536 addresses to check

    Attributes
    ----------
    start_ip_address : str
        First IP address to check. If only one address needs checking,
        do not set end_ip_address.
    start_port : int
        First port to check. If only one port needs checking,
        do not set end_port
    end_ip_address : str or None
        End address (inclusive). If not specified (default),
        only check one address
    end_port : int or None
        End port (inclusive). If not specified (default), only check one port.
    """
    def __init__(self, start_ip_address, start_port,
                 end_ip_address=None, end_port=None):
        self.start_ip_address = start_ip_address
        self.start_port = start_port
        self.end_ip_address = end_ip_address or self.start_ip_address
        self.end_port = end_port or self.start_port

    def get_ip_addresses(self):
        """Get range of addresses

        Returns
        -------
        addresses : iterable of str
        """
        addresses = []
        current_address = IPAddress(self.start_ip_address)
        last_address = IPAddress(self.end_ip_address)
        while current_address <= last_address:
            yield str(current_address)
            current_address.incr()

    def get_ports(self):
        """Get range of ports

        Returns
        -------
        ports : iterable of int
        """
        return range(self.start_port, self.end_port+1)

    def get_registry(self):
        """Checks the IPs and ports for the registry"""
        ports = self.get_ports()
        for ip_address in self.get_ip_addresses():
            for port in ports:
                found_address, found_port = self.check_ip(ip_address, port)
                if found_address is not None:
                    return self.found_registry(found_address, found_port)
        return None
