from config import FrameworkPaths
from src.devices.device_parser import DevicesParser

DEVICES: dict[str, dict] = DevicesParser(FrameworkPaths.DEVICES_YAML).devices
