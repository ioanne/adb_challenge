import io
from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import StreamingResponse

from app.services.adb.client.powered_client import get_adb_client

router = InferringRouter()


@cbv(router)
class DeviceViews:

    @property
    def client(self):
        return get_adb_client()

    def _get_device(self, device_serial):
        device = self.client.device(device_serial)
        if not device:
            raise HTTPException(status_code=404, detail='Device not found.')
        return device

    @router.get("/devices/")
    async def get_devices(self):
        return self.client.devices() or []

    @router.get("/device/{device_serial}/")
    async def get_device(self, device_serial: str):
        return self._get_device(device_serial)

    @router.get("/device/{device_serial}/screenshot/")
    async def get_screenshot(self, device_serial: str):
        device = self._get_device(device_serial)
        screen = device.screencap()
        if screen:
            return StreamingResponse(io.BytesIO(screen), media_type="image/png")
        return {}

    @router.get("/device/{device_serial}/logs/")
    async def get_logs(self, device_serial: str):
        device = self._get_device(device_serial)
        return device.get_log()
