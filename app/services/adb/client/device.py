import logging

from ppadb.device import Device

from datetime import datetime

logger = logging.get_logger(__name__)


class PoweredDevice(Device):

    def open_app(self, app):
        "com.android.chrome/com.google.android.apps.chrome.Main"
        self.shell(f'am start -n {app}')

    def get_log(self):
        return self.shell('logcat -d')

    def take_screen(self):
        timestamp = str(datetime.timestamp(datetime.now()))
        file_name = f'/sdcard/screen-{timestamp}.png'
        screen = self.screencap()
        with open(file_name, "wb") as fp:
            fp.write(screen)
        return fp
