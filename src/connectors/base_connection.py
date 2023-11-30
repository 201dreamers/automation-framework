import re
import threading
from time import sleep, time
from abc import ABC, abstractmethod

from config import stdout_logger
from src.connectors.exceptions import ReadTimeoutError


class BaseConnection(ABC):
    """Base connection library containing higher level functions

    This library cannot be used alone. The individual connection specific read
    and write functions must be defined in the inherited child class.
    """

    SHELL_PROMPT = r"\[\w+@\w+\] [/\w]*> "

    def __init__(self):
        self.lock = threading.Lock()

    def __del__(self):
        """Closes the connection when the object is destroyed."""
        self.close_connection()

    @abstractmethod
    def open_connection(self):
        """Opens the connection"""
        ...

    @abstractmethod
    def close_connection(self):
        """Closes the connection"""
        ...

    @abstractmethod
    def is_connected(self):
        """Checks the connection status"""
        ...

    @abstractmethod
    def output_available(self):
        """The status of the output buffer for reads."""
        ...

    @abstractmethod
    def get_read_timeout(self) -> float:
        """Gets the read timeout
        :return:
            - timeout: The timeout in seconds
        """
        ...

    @abstractmethod
    def set_read_timeout(self, timeout: float):
        """Sets the read timeout
        :param timeout: The timeout in seconds
        """
        ...

    @abstractmethod
    def write(self, data: str):
        """Writes the data to the shell
        :param data: Data to write to the shell
        """
        ...

    @abstractmethod
    def read(self, count: float = 1) -> bytes:
        """Reads the data from the shell
        :param count: Number of bytes to read from the shell
        :return:
            - data: The data read
        """
        ...

    def writeln(self, data: str = ""):
        """Writes the data to the shell with a newline
        :param data: Data to write to the shell
        """
        self.write(f"{data}\r\n")

    def restart_connection(self):
        """Restarts the connection by closing and reopening it."""
        self.close_connection()
        self.open_connection()

    def send_command(self, command: str, timeout: float = 15, strip: bool = True) -> str:
        """Sends a command and waits for the shell prompt within
        the desired timeout

        :param command: The string command
        :param timeout: The timeout before the prompt is read
        :return:
            - response: The returned output
        """
        try:
            self.lock.acquire()
            self.clear_output_buffer()

            stdout_logger.info(f"=> {command}")
            self.writeln(command)
            self.read_until_prompt(timeout)

            data = self.read_until_prompt(timeout)
            stdout_logger.debug(f"Raw response: <{data}>")
            response = self._extract_response(command, data)

            self.clear_output_buffer()
        finally:
            self.lock.release()

        response = response.strip() if strip else response
        stdout_logger.info(f"=< {response}")

        return response

    def read_until(self, expected: str, timeout: float = 5) -> str:
        """Reads the shell until the expected string
        :param expected: The expected string
        :param timeout: The timeout
        :return:
            - output: The read output
        :raise:
            - ReadTimeout: If the expected string is not read in time
        """
        max_time = time() + timeout
        expected_bytes = expected.encode()
        output = b""
        while time() < max_time:
            output += self.read(1)
            if expected_bytes in output:
                return output.decode()
        raise ReadTimeoutError(f"Expected '{expected}' in {timeout} seconds. "
                               f"Only read '{output.decode().strip()}'")

    def read_until_regexp(self, expected: str, timeout: float = 5):
        """Reads the shell until the regular expression
        :param expected: The expected regular expression
        :param timeout: The timeout
        :raise:
            - ReadTimeout: If the expected string is not read in time
        """
        max_time = time() + timeout
        regexp = re.compile(expected)
        output = b""
        while time() < max_time:
            output += self.read(1)
            try:
                if regexp.search(output.decode()):
                    return output.decode()
            except UnicodeDecodeError:
                pass  # Bytes read is not complete
        raise ReadTimeoutError(f"Expected '{expected}' in {timeout} seconds. "
                               f"Only read '{output.decode().strip()}'")

    def read_until_prompt(self, timeout: float = 5) -> str:
        """Reads the shell until the shell prompt
        :param timeout: The timeout
        :return:
            - output: The read output
        :raise:
            - ReadTimeout: If the expected string is not read in time
        """
        output = self.read_until_regexp(self.prompt, timeout)
        return output

    def clear_output_buffer(self, timeout: float = 0.5):
        """Clears the output buffer by reading
        The timeout is the amount of time to wait since
        the last read. It is reset every time new data is read
        :param timeout: The timeout
        """
        max_time = time() + timeout
        while time() < max_time:
            if self.output_available():
                self.read()
                max_time = time() + timeout

    def _extract_response(self, command: str, data: str) -> str:
        """Extract the response from the data read from the shell
        The response is in the format of
            `<command>\\n\\r<response>[admin@...] > `
        The response is the substring of starting from the command + newline end
        to the beginning of username
        :param command: The command sent
        :param data: The data returned from the shell
        :return:
            - response: The returned output
        """

        # Clean Command and Data
        command = re.sub(r"[^\r]\n", r"\r\n", command)  # missing carriage return
        data = re.sub(r"\r\n>;? ", "\r\n", data)  # block responses
        data = re.sub(r"\'", "'", data)  # escaped quotes

        start = data.find(command) + len(command) + 1  # 1 is new line character length
        end = data.rfind("[admin@")
        response = data[start:end]

        return response

    def _run_test_command(self) -> tuple[bool, str]:
        """Runs test command and compares output
        :return:
            - success: test result status
            - response: response
        """
        self.send_command("beep")
        response = self.send_command("system identity print")
        success = response == "name: MikroTik"
        stdout_logger.info(f"Initial test finished. Successful: {success}")
        return success, response
