
from servicediscovery.methods import Method


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
