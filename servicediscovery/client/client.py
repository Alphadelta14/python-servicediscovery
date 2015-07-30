
"""
    ServiceClient
    A client representation of itself and other registered services

    Author: Alpha <alpha@projectpokemon.org>
"""

import servicediscovery.client

__all__ = ['ServiceClient', 'RegisteredServiceClient']


class ServiceClientError(Exception):
    """Raised for errors in ServiceClient"""
    pass


class ServiceClient(object):
    """Service Client capable of discovering a registry and making
    itself known.

    Attributes
    ----------
    service_type : str
        Prefix/namespace of the service
    service_id : int or None
        Unique identifier of the service when registered
    methods : list of Method
        Methods to discover the registry
    registry : Registry or None
        Registry when registered
    """
    def __init__(self, service_type):
        self.service_type = service_type
        self.service_id = None
        self.methods = []
        self.registry = None
        self.retry_all = 3

    def get_name(self):
        """Get the name of the registered service

        Returns
        -------
        service_name : str

        Raises
        ------
        ServiceClientError
            If the service is not yet registered with the registry
        """
        if self.service_id is None:
            raise ServiceClientError('This service is not registered')
        return '{type}:{id}'.format(type=self.service_type,
                                    id=self.service_id)

    def on_register(self, registry):
        """Callback when register() is called with block=False

        This will be called in a new thread.

        Parameters
        ----------
        registry : Registry
        """
        pass

    def register(self, block=True):
        """Find the control node based on the provided methods and registers
        with it.

        Parameters
        ----------
        block : Boolean, optional
            If block is True (default), this will block until the control
            node is found. Otherwise, this will call self.on_register()
            in a new thread

        Returns
        -------
        registry : Registry or None
            The discovered registry or None if not blocking
        """
        if not block:
            # TODO: Async?
            raise NotImplementedError('Asynchronous mode not implemented')
        for retry in range(self.retry_all):
            for method in self.methods:
                registry = method.register(self)
                if registery is not None:
                    return registery
        raise ServiceClientError('Could not find a registry')

    def add_method(self, method):
        """Adds a Method to be checked for discovering the registry

        Parameters
        ----------
        method : Method
        """
        self.methods.append(method)


class RegisteredServiceClient(ServiceClient):
    """A registered ServiceClient as returned by the ServiceRegistry
    """
    def __init__(self, service_type, service_id, registry):
        ServiceClient.__init__(self, service_type)
        self.service_id = service_id
        self.registry = registry

    def register(self, block=True):
        """Registration is not allowed for RegisteredServiceClient

        Raises
        ------
        ServiceClientError
            This is not an allowed method
        """
        raise ServiceClientError('Cannot register a registered service')
