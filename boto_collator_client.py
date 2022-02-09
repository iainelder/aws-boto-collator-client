__version__ = "0.2.0"


class CollatorClient(object):
    def __init__(self, client):
        self._client = client

    def __getattr__(self, name):
        """
        Implements __getattr__ to intercept all method lookups in the same way.

        Lookups for anything other than a paginated API are delegated to the original client.
        This delegation must use __getattribute__ rather than __getattr__ for reasons I don't
        fully understand. I think it's because the list of methods is generated dynamically.

        If the method is a paginated API, it gets the paginator for the method and uses it
        to build a collator.
        """
        if _has_paginated_api(self._client, name):
            return _build_collator(self._client.get_paginator(name))
        else:
            return self._client.__getattribute__(name)


def _has_paginated_api(client, method):
    """
    Returns true if the method maps to a paginated API.
    Returns false otherwise.
    This wrapper is necessary because a client's can_paginate returns a
    KeyError when the input is not an API method.
    """
    # return method in client.meta.method_to_api_mapping and client.can_paginate(method)
    try:
        return client.can_paginate(method)
    except KeyError:
        return False


def _build_collator(paginator):
    """
    Returns a callable that returns the full result for the paginator.
    """

    def collate(*args, **kwargs):
        it = paginator.paginate(*args, **kwargs)
        full_result = it.build_full_result()
        return full_result

    return collate
