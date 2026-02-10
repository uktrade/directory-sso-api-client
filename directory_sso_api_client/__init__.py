from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('sso_api_client')
except PackageNotFoundError:
    __version__ = 'dev'

from directory_sso_api_client.client import sso_api_client

__all__ = ['sso_api_client']
