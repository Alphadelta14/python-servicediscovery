
"""
    DNSMethod
    Use DNS to determine the location of the registry node

    Author: Alpha <alpha@projectpokemon.org>
"""

import socket

from servicediscovery.methods import Method


class DNSMethod(Method):
    """Checks a DNS RR for the registry

    Attributes
    ----------
    hostname : str
    port : int
    """
    def __init__(self, hostname, port):
        self.hostname = hostname
        # TODO: dns servers
        self.port = port

    def get_registry(self):
        """Checks the addresses for a given hostname"""
        for (family, socktype, proto, canonname, sockaddr) in \
                socket.getaddrinfo(self.hostname, self.port, 0, 0,
                                   socket.IPPROTO_TCP):
            ip_address, port = sockaddr[:2]
            found_address, found_port = self.check_ip(ip_address, port,
                                                      family=family)
            if found_address is not None:
                return self.found_registry(found_address, found_port)
        return None
