import io
from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import StreamingResponse
from pydantic import BaseModel

from app.services.adb.client.powered_client import get_adb_client

router = InferringRouter()


class AndroidApp(BaseModel):
    app_id: str


class InstallAppData(BaseModel):
    path: str


@cbv(router)
class DeviceViews:

    @property
    def client(self):
        return get_adb_client()

    def _get_device(self, device_serial):
        """Search and return a device.
        If it does not exist an HTTPException is thrown.
        :"""
        device = self.client.device(device_serial)
        if not device:
            raise HTTPException(status_code=404, detail='Device not found.')
        return device

    @router.get("/devices/")
    async def get_devices(self):
        """Endpoint to get all devices."""
        return self.client.devices() or []

    @router.get("/device/{device_serial}/")
    async def get_device(self, device_serial: str):
        """Endpoint to get a specific device by serial."""
        return self._get_device(device_serial)

    @router.get("/device/{device_serial}/screenshot/")
    async def get_screenshot(self, device_serial: str):
        """Endpoint to get a screen shot inside a device by serial."""
        device = self._get_device(device_serial)
        screen = device.screencap()
        if screen:
            return StreamingResponse(io.BytesIO(screen), media_type="image/png")
        return {}

    @router.get("/device/{device_serial}/logs/")
    async def get_logs(self, device_serial: str):
        """Endpoint to get logs inside a device by serial."""
        device = self._get_device(device_serial)
        return {'logs': device.get_log()}

    @router.post("/device/{device_serial}/open_app/")
    async def open_app(self, device_serial: str, android_app: AndroidApp):
        """Endpoint to open app inside a device by serial."""
        device = self._get_device(device_serial)
        message = device.open_app(android_app.app_id)
        if 'Error type' in message:
            raise HTTPException(status_code=406, detail=message)
        return {}

    @router.post("/device/{device_serial}/install/")
    async def install_apk(self, device_serial: str, install_app_data: InstallAppData):
        """Endpoint to install app inside a device by serial."""
        device = self._get_device(device_serial)
        try:
            was_installed = device.install(install_app_data.path)
        except IOError:
            raise HTTPException(status_code=406, detail='Cannot find path.')
        return was_installed
