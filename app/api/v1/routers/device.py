from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.adb.client.powered_client import get_adb_client

router = InferringRouter()


@cbv(router)
class DeviceViews:

    @property
    def client(self):
        return get_adb_client()

    @router.get("/devices/")
    async def get_devices(self):
        return self.client.devices() or []

    @router.get("/device/{device_serial}/")
    async def get_device(self, device_serial: str):
        device = self.client.device(device_serial)
        if not device:
            raise HTTPException(status_code=404, detail='Device not found.')
        return device
