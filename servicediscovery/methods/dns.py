
"""
    DNSMethod
    Use DNS to determine the location of the registry node

    Author: Alpha <alpha@projectpokemon.org>
"""

import socket
import struct

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

    def get_candidates(self):
        """Does a DNS lookup and returns the potential get_candidates

        Returns
        -------
        candidates : List of (ip_address, port, family)
        """
        candidates = []
        for (family, socktype, proto, canonname, sockaddr) in \
                socket.getaddrinfo(self.hostname, self.port, 0, 0,
                                   socket.IPPROTO_TCP):
            candidates.append(sockaddr[:2]+(family,))
        return candidates

    def get_registry(self):
        """Checks the addresses for a given hostname"""
        for ip_address, port, family in self.get_candidates():
            found_address, found_port = self.check_ip(ip_address, port,
                                                      family=family)
            if found_address is not None:
                return self.found_registry(found_address, found_port)
        return None


class MDNSMethod(DNSMethod):
    """Uses multicast DNS to check local network for target

    See Also
    --------
    DNSMethod
    """
    def get_candidates(self):
        mdns_groups = [(socket.AF_INET, '224.0.0.251'),
                       ]  # (socket.AF_INET6, 'FF02::FB')]
        mdns_port = 5353

        for family, mdns_group in mdns_groups:
            sock = socket.socket(family, socket.SOCK_DGRAM,
                                 socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', mdns_port))
            mdns_group_repr = socket.inet_pton(family, mdns_group)
            # TODO: IPv6
            ip_mreqn = struct.pack('4sll', mdns_group_repr,
                                   socket.INADDR_ANY, 0)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                            ip_mreqn)

        while True:
            print(sock.recv(10240), )
