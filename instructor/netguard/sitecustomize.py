"""Network guard for verification runs. Python imports this file at start-up when its
folder is on PYTHONPATH, so every Python child process, and every Python process those
children start, inherits it. Connections to loopback addresses and Unix sockets work;
any other connect, and any name lookup for a non-loopback host, raises NetworkBlocked.
Standard library only.
"""
import socket

LOOPBACK = ("127.", "::1", "localhost")


class NetworkBlocked(OSError):
    """Raised when a connection would leave the loopback interface."""


def _is_loopback(host):
    return isinstance(host, str) and host.startswith(LOOPBACK)


_real_connect = socket.socket.connect
_real_connect_ex = socket.socket.connect_ex
_real_getaddrinfo = socket.getaddrinfo


def _check(sock, address):
    """Raise NetworkBlocked for an internet socket aimed outside the loopback."""
    if sock.family in (socket.AF_INET, socket.AF_INET6):
        if not _is_loopback(address[0]):
            raise NetworkBlocked(f"connect to {address[0]} blocked")


def _connect(self, address):
    _check(self, address)
    return _real_connect(self, address)


def _connect_ex(self, address):
    _check(self, address)
    return _real_connect_ex(self, address)


def _getaddrinfo(host, *args, **kwargs):
    if host is not None and not _is_loopback(host):
        raise NetworkBlocked(f"name lookup for {host} blocked")
    return _real_getaddrinfo(host, *args, **kwargs)


socket.socket.connect = _connect
socket.socket.connect_ex = _connect_ex
socket.getaddrinfo = _getaddrinfo
