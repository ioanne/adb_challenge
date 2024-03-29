import logging

from ppadb.device import Device

from datetime import datetime

logger = logging.getLogger(__name__)


class PoweredDevice(Device):

    def open_app(self, app):
        """ Example: com.android.chrome/com.google.android.apps.chrome.Main"""
        return self.shell(f'am start -n {app}')

    def get_log(self):
        return self.shell('logcat -d')

    def take_screen(self):
        timestamp = str(datetime.timestamp(datetime.now()))
        file_name = f'app/screen-{timestamp}.png'
        screen = self.screencap()
        with open(file_name, "wb") as fp:
            fp.write(screen)
        return fp
