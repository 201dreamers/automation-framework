"""Library to enable connection to the device through SSH"""
import logging
import os

from paramiko import AutoAddPolicy, SSHClient
from paramiko.channel import Channel
from paramiko.config import SSHConfig

from config import stdout_logger
from src.connectors.base_connection import BaseConnection
from src.connectors.exceptions import ConnectionTestError, ReadTimeoutError


class SSHConnection(BaseConnection):
    """Library to enable connection to the device through SSH."""

    def __init__(
        self, ip_address: str, username: str, password: str | None = None,
        port: int = 22, timeout: float = 10
    ):
        """Initializes the SSH connection

        Let me root needs to be present on the device for this connection
        method to work.
        """
        super().__init__()

        self.ip_address = ip_address
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.shell = None

        self.prompt = self.SHELL_PROMPT

        logging.basicConfig()
        logging.getLogger("paramiko").setLevel(logging.DEBUG)

    @staticmethod
    def get_config_file() -> SSHConfig | None:
        """Gets the config file from the user
        :return:
            - ssh_config: SSH config file
        """
        ssh_config = SSHConfig()
        ssh_config_file = os.path.expanduser("~/.ssh/config")

        if not os.path.isfile(ssh_config_file):
            return

        with open(ssh_config_file) as file:
            ssh_config.parse(file)

        return ssh_config

    def open_connection(self):
        """Opens the SSH connection and establishes a shell
        :raises:
            - ConnectionTestError if the login to the shell and echo command is not
                successful
        """
        stdout_logger.info(f"Connecting to device {self.ip_address}:{self.port}")
        self.client.connect(
            hostname=self.ip_address,
            port=self.port,
            username=self.username,
            password=self.password,
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )

        self.shell = self._create_shell()
        self.set_read_timeout(self.timeout)

        success, response = self._run_test_command()
        if not success:
            raise ConnectionTestError(f"Device connection test failed. Response: {repr(response)}")
        stdout_logger.success("Connection established\n")

    def is_connected(self) -> bool:
        """Checks the connection status."""
        if self.client.get_transport() is not None:
            return self.client.get_transport().is_active()
        return False

    def _create_shell(self) -> Channel:
        shell = self.client.invoke_shell(term="vt100", width=512, height=24)
        return shell

    def close_connection(self):
        """Closes the connection."""
        stdout_logger.info(f"Closing connection to device {self.ip_address}:{self.port}")
        if self.is_connected():
            try:
                self.send_command("quit", timeout=1)
            except ReadTimeoutError:
                stdout_logger.info("Console is no longer accessible")
        self.client.close()
        stdout_logger.success("Connection closed\n")

    def write(self, data: str):
        """Writes the data to the shell
        :param data: Data to write to the shell
        """
        self.shell.sendall(data)

    def read(self, count: int = 1) -> bytes:
        """Reads the data from the shell
        :param count: Number of bytes to read from the shell
        :return:
            - data: The data read (bytes)
        """
        data = b""
        if self.output_available():
            data = self.shell.recv(count)
        return data

    def output_available(self) -> bool:
        """The status of the output buffer for reads."""
        return self.shell.recv_ready()

    def get_read_timeout(self) -> float:
        """Gets the read timeout
        :return:
            - timeout: The timeout in seconds (int, float)
        """
        return self.shell.gettimeout()

    def set_read_timeout(self, timeout: float):
        """Sets the read timeout
        :param timeout: The timeout in seconds (int, float)
        """
        self.shell.settimeout(timeout)
