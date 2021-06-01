import logging

from app.services.adb.client import get_adb_client

logger = logging.getLogger(__name__)


class Devices:

    def __init__(self):
        self.client = get_adb_client()

    def get_all(self):
        """Returns a list of devices."""
        logger.info('Getting all devices')
        return self.client.devices()

