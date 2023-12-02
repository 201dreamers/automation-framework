from yaml import safe_load

from config import DeviceSecrets, FrameworkPaths
from src.connectors import (BaseConnection, ConnectionType,
                            NoSuchConnectionTypeError, SerialConnection,
                            SSHConnection)
from src.device_lib.exceptions import (NoSuchCommandError, NoSuchDeviceError,
                                       NoSuchSubCommandError)
from src.devices import DEVICES


class Command:
    def __init__(self, connection: BaseConnection, name: str, sub_commands: dict | None = None):
        self.connection = connection
        self.name = name
        self._sub_commands = sub_commands

    def __getattr__(self, name) -> "Command":
        sub_command = self._sub_commands.get(name) if self._sub_commands else None
        if sub_command is None:
            raise NoSuchSubCommandError(self.name, name)

        return sub_command

    def __call__(self, *args, **kwargs) -> str:
        arguments = " ".join(args)
        return self.connection.send_command(f"{self.name} {arguments}")


class DeviceConnection:
    def __init__(self, connection_type: ConnectionType, device_name: str):
        self.device = DEVICES.get(device_name)
        if self.device is None:
            raise NoSuchDeviceError(device_name)

        if connection_type is ConnectionType.SSH:
            self.connection = SSHConnection(
                self.device["ip"],
                DeviceSecrets.USERNAME,
                DeviceSecrets.PASSWORD,
                self.device["ssh_port"]
            )
        elif connection_type is ConnectionType.SERIAL:
            self.connection  = SerialConnection(
                self.device["serial_port"],
                DeviceSecrets.USERNAME,
                DeviceSecrets.PASSWORD,
                self.device["baudrate"]
            )
        else:
            raise NoSuchConnectionTypeError(connection_type)

        self.connection.open_connection()

    def __del__(self):
        self.connection.close_connection()


class DeviceLib(DeviceConnection):
    def __init__(self, connection_type: ConnectionType, device_name: str):
        super().__init__(connection_type, device_name)
        self._commands =self._parse_commands()

    def __getattr__(self, name: str) -> Command:
        command = self._commands.get(name)
        if command is None:
            raise NoSuchCommandError(name)
        return command

    def _parse_commands(self) -> dict[str, Command]:
        raw_cmds = self._load_raw_commands()
        commands = {}
        for cmd_name, sub_cmds in raw_cmds.items():
            commands.update(self._create_command(cmd_name, sub_cmds))

        return commands

    def _create_command(self, name: str, sub_commands: dict | None = None) -> dict[str, Command]:
        sub_command_objects = None

        if sub_commands:
            sub_command_objects = {}
            for sub_cmd_name, sub_sub_cmd in sub_commands.items():
                sub_command_objects = self._create_command(sub_cmd_name, sub_sub_cmd)

        command_obj = Command(self.connection, name, sub_command_objects)
        return {name: command_obj}

    @staticmethod
    def _load_raw_commands() -> dict[str, dict | None]:
        with open(FrameworkPaths.COMMANDS_YAML) as fobj:
            return safe_load(fobj.read())
