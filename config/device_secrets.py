import os


class DeviceSecrets:
    USERNAME = os.getenv("DEVICE_USERNAME", "admin")
    PASSWORD = os.getenv("DEVICE_PASSWORD")
