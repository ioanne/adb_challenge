import logging

from app.services.adb.client import get_adb_client

logger = logging.getLogger(__name__)


class Devices:

    class CouldNotInstallException(Exception):
        pass

    def __init__(self):
        self.client = get_adb_client()

    def get_all(self):
        """Returns a list of devices."""
        logger.info('Getting all devices')
        return self.client.devices()

    def install_apk(self, apk_path, device=None):
        was_installed = device.install(apk_path)
        if not was_installed:
            raise Devices.CouldNotInstallException("The apk could not installed.")
        return was_installed
