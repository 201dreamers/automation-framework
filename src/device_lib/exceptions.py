class NoSuchDeviceError(Exception):
    def __init__(self, device_name: str):
        self.device_name = device_name

    def __str__(self):
        return f"{self.device_name} device doesn't exist"


class NoSuchCommandError(Exception):
    def __init__(self, cmd_name: str):
        self.cmd_name = cmd_name

    def __str__(self):
        return f"{self.cmd_name} command doesn't exist"


class NoSuchSubCommandError(Exception):
    def __init__(self, cmd_name: str, sub_cmd_name: str):
        self.cmd_name = cmd_name
        self.sub_cmd_name = sub_cmd_name

    def __str__(self):
        return f"Subcommand {self.sub_cmd_name} doesn't exist under {self.sub_name} command"
