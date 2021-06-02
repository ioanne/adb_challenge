from ppadb.client import Client as AdbClient

from app.services.adb.client.device import PoweredDevice

ADB_CLIENT_IP = '127.0.0.1'
ADB_CLIENT_PORT = 5037


def get_adb_client():
    """The adb client is returned without re-instantiating it."""
    if not getattr(get_adb_client, '_cached_client', None):
        get_adb_client._cached_client = PoweredClient(
            host=ADB_CLIENT_IP,
            port=ADB_CLIENT_PORT
        )
    return get_adb_client._cached_client


class PoweredClient(AdbClient):
    
    def devices(self, state=None):
        cmd = "host:devices"
        result = self._execute_cmd(cmd)

        devices = []

        for line in result.split('\n'):
            if not line:
                break

            tokens = line.split()
            if state and len(tokens) > 1 and tokens[1] != state:
                continue

            devices.append(PoweredDevice(self, tokens[0]))

        return devices
