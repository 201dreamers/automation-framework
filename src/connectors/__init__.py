from enum import Enum

from src.connectors.base_connection import BaseConnection
from src.connectors.exceptions import NoSuchConnectionTypeError
from src.connectors.serial_connection import SerialConnection
from src.connectors.ssh_connection import SSHConnection


class ConnectionType(Enum):
    SSH = "ssh"
    SERIAL = "serial"
