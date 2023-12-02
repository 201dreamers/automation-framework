"""Connection error exceptions"""

class ReadTimeoutError(Exception):
    def __init__(self, expected: str, got: str, timeout: float):
        self.expected = expected
        self.got = got
        self.timeout = timeout

    def __str__(self):
        return f"Expected '{self.expected}' in {self.timeout} seconds. Only read '{self.got}'"


class ConnectionTestError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Device connection test failed. Response: {repr(self.response)}"


class ConnectionClosedError(Exception):
    def __str__(self):
        return "Connection is closed"
