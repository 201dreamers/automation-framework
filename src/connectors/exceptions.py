"""Connection error exceptions"""


class Error(Exception):
    def __init__(self, message):
        self.message = message


class ReadTimeoutError(Error):
    pass


class ConnectionTestError(Error):
    pass


class ConnectionClosedError(Error):
    pass
