from config.devices.device_parser import DevicesParser
from config.paths import FrameworkPaths

DEVICES: dict[str, dict] = DevicesParser(FrameworkPaths.DEVICES_YAML).devices
