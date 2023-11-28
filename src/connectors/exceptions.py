"""Connection error exceptions"""
# ruff: disable=too-few-public-methods,missing-docstring,super-init-not-called


class Error(Exception):
    def __init__(self, message):
        self.message = message


class ReadTimeoutError(Error):
    pass


class ConnectionTestError(Error):
    pass


class ConnectionClosedError(Error):
    pass
