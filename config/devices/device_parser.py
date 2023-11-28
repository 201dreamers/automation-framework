from pathlib import Path

from yaml import safe_load


class DevicesParser:
    """Parses yaml file with described devices.
    The file should have default section, where all default fields are
    determined. If some device doesn't contain some field, the default field
    will be used.
    """

    def __init__(self, devices_yaml: Path):
        raw_devices = self._load_devices(devices_yaml)
        self._default: dict = raw_devices.pop("default")

        self.devices: dict[str, dict] = {}
        for device, config in raw_devices.items():
            self.devices[device] = self.update_config_with_default_values(config)

    def update_config_with_default_values(self, config: dict) -> dict:
        for key, val in self._default.items():
            if key not in config:
                config[key] = val

        return config

    @staticmethod
    def _load_devices(devices_yaml: Path) -> dict[str, dict]:
        with devices_yaml.open("r") as fobj:
            devices = safe_load(fobj.read())

        return devices
