
"""
    ServiceRegistry
    A client representation of the service registry

    Author: Alpha <alpha@projectpokemon.org>
"""

import servicediscovery.client

__all__ = ['ServiceRegistry']


class ServiceRegistry(object):
    """Representation of the registry visible to services

    Attributes
    ----------
    clients : list of ServiceClient
        Known services
    """
    def __init__(self):
        self._clients = []

    @property
    def clients(self):
        """List of clients
        """
        raise NotImplementedError()
        return self._clients

    def locate(self, service_type, service_id=None):
        """Find a ServiceClient for a specified type

        Parameters
        ----------
        service_type : str
            Type of the service to lookup
        service_id : int or None
            If specified, this will look for an exact service_id.
            Otherwise, this will look for any matching service

        Returns
        -------
        service : RegisteredServiceClient
        """
        pass
