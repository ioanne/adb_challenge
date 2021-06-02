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
