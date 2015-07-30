
"""
    Method
    Ways to detect the registry node

    Author: Alpha <alpha@projectpokemon.org>
"""

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
        pass
