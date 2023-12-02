import os
from pathlib import Path


class FrameworkPaths:
    FRAMEWORK_ROOT = Path(os.getenv("FRAMEWORK_DIR", os.getcwd()))
    CONFIG_DIR = FRAMEWORK_ROOT / "config"
    RESOURCES_DIR = FRAMEWORK_ROOT / "resources"
    REPORTS_DIR = FRAMEWORK_ROOT / "reports"

    DEVICES_YAML = RESOURCES_DIR / "devices.yaml"
    COMMANDS_YAML = RESOURCES_DIR / "console_commands.yaml"
