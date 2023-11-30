import os
from pathlib import Path


class FrameworkPaths:
    FRAMEWORK_ROOT = Path(os.getenv("FRAMEWORK_DIR", os.getcwd()))
    CONFIG_DIR = FRAMEWORK_ROOT / "config"
    DEVICES_YAML = CONFIG_DIR / "devices" / "devices.yaml"
    REPORTS_DIR = FRAMEWORK_ROOT / "reports"
