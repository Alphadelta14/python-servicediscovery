
"""
    Method
    Ways to detect the registry node

    Author: Alpha <alpha@projectpokemon.org>
"""

import socket

from servicediscovery.client import ServiceRegistry

__all__ = ['Method']


class Method(object):
    """A registry lookup method"""
    def register(self, client):
        """Register with a registry via this method

        Parameters
        ----------
        client : ServiceClient
            Client to try registering from

        Returns
        -------
        registry : ServiceRegistry or None
            the registry if found
        """
        registry = self.get_registry()
        registry._clients.append(client)
        return registry

    def get_registry(self):
        """Get a registry. Not available for the base class"""
        raise NotImplementedError('Cannot find a registry with no method')

    @staticmethod
    def found_registry(ip_address, port):
        """Factory that returns a registry after finding it

        Parameters
        ----------
        ip_address : str
            Address of the service
        port : int
            Port of the service
        """
        registry = ServiceRegistry()
        registry.ip_address = ip_address
        registry.port = port
        return registry

    @staticmethod
    def check_ip(ip_address, port):
        """Checks that an IP:port is open

        Parameters
        ----------
        ip_address : str
            Address to check
        port : int
            Port to check

        Returns
        -------
        ip_address, port : (str, int) or (None, None)
        """
        # TODO: IPv6 family
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)  # TODO: configurable
        try:
            sock.connect((ip_address, port))
        except:
            return None, None
        else:
            pass  # TODO: acknowledge
        finally:
            sock.close()
        return ip_address, port
