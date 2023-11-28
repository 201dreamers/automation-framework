"""Library to enable connection to the device through serial"""
import time

import serial

from src.connectors.base_connection import BaseConnection
from src.connectors.exceptions import ConnectionTestError


class SerialConnection(BaseConnection):
    """Library to enable connection to the device through serial."""

    def __init__(
        self, port: int, username: str, password: str | None = None,
        baudrate: int = 115200, timeout: float = 2
    ):
        """Initializes the serial connection instance

        Let me root needs to be present on the device for this connection
        method to work.
        """
        super().__init__()

        self.timeout = timeout

        self.connection = serial.Serial()
        self.connection.port = port
        self.connection.baudrate = baudrate
        self.username = username
        self.password = password
        self.set_read_timeout(timeout)

        self.prompt = self.SHELL_PROMPT

    def check_and_login(self):
        # Enter newline to check for login prompt
        self.clear_output_buffer()
        self.writeln()
        response = self.read(150).decode()

        # Check for login prompt and login
        if "Login: " in response:
            self.clear_output_buffer()
            self.writeln(self.username)
            self.read_until("Password: ")
            self.writeln(self.password)
        else:
            self.writeln()

        self.read_until_prompt()

    def open_connection(self):
        """Opens the serial connection
        :raises:
            - ConnectionTestError if the login to the shell and echo command is not
                successful
        """
        self.connection.open()
        self.check_and_login()

        success, response = self._run_test_command()
        if not success:
            raise ConnectionTestError(f"Device connection test failed. Response: {repr(response)}")

    def close_connection(self):
        """Closes the connection."""
        if self.is_connected():
            self.writeln("stty echo")
            self.clear_output_buffer()

        self.connection.close()

    def is_connected(self) -> bool:
        """Checks the connection status."""
        return self.connection.is_open

    def reboot(self):
        self.writeln("reboot")
        self.read_until("login: ", timeout=180)

        self.check_and_login()

    def write(self, data: str):
        """Writes the data to the shell
        :param data: Data to write to the shell
        """
        self.connection.write(data.encode())
        self.connection.flush()
        time.sleep(0.05)  # implicit sleep for all writes

    def read(self, count: int = 1) -> bytes:
        """Reads the data from the shell"""
        data = b""
        if self.output_available():
            data = self.connection.read(count)
        return data

    def output_available(self) -> bool:
        """The status of the output buffer for reads"""
        return bool(self.connection.in_waiting)

    def get_read_timeout(self) -> float:
        """Gets the read timeout"""
        return self.connection.timeout

    def set_read_timeout(self, timeout: float):
        """Sets the read timeout"""
        self.connection.timeout = timeout
