""" Backend abstraction """
from importlib import import_module
from django.conf import settings


def openedx_bearer_authentication(*args, **kwargs):  # pylint: disable=unused-argument
    """ Get openedx Bearer authentication method. """

    backend_function = settings.OPR_OPENEDX_AUTHENTICATION
    backend = import_module(backend_function)

    return backend.BearerAuthentication
