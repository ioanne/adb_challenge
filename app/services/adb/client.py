from ppadb.client import Client as AdbClient

ADB_CLIENT_IP = '127.0.0.1'
ADB_CLIENT_PORT = 5037


def get_adb_client():
    """The adb client is returned without re-instantiating it."""
    if not getattr(get_adb_client, '_cached_client', None):
        get_adb_client._cached_client = AdbClient(
            host=ADB_CLIENT_IP,
            port=ADB_CLIENT_PORT
        )
    return get_adb_client._cached_client
