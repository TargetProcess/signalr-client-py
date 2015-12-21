from gevent import monkey

monkey.patch_socket()

from ._connection import Connection

__version__ = '0.0.6'
