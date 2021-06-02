from io import BytesIO
from fastapi.testclient import TestClient
from unittest import mock, TestCase
from PIL import Image

from app.api.v1.main import app
from app.services.adb.client.device import PoweredDevice

client = TestClient(app)

class DeviceEndpointTestCase(TestCase):

    def _create_test_image(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    @mock.patch('app.api.v1.routers.device.get_adb_client')
    def test_get_devices_successful(self, client_mock):
        expected_response = [
            {
                'client': {
                    'host': '127.0.0.1', 'port': 5037
                },
                'serial': 'emulator-5559'
            }
        ]
        device_mock = mock.MagicMock()
        device_mock.devices.return_value = expected_response
        client_mock.return_value = device_mock
        
        response = client.get("/devices/")
        assert response.status_code == 200
        assert response.json() == expected_response

        device_mock = mock.MagicMock()
        device_mock.devices.return_value = []
        client_mock.return_value = device_mock
        
        response = client.get("/devices/")
        assert response.status_code == 200
        assert response.json() == []


    @mock.patch('app.api.v1.routers.device.get_adb_client')
    def test_get_device_successful(self, client_mock):
        expected_response = {
            'client': {
                'host': '127.0.0.1', 'port': 5037
            },
            'serial': 'emulator-5559'
        }
        
        device_mock = mock.MagicMock()
        device_mock.device.return_value = expected_response
        client_mock.return_value = device_mock
        
        response = client.get("/device/emulator-5559/")
        print(response.status_code)
        assert response.status_code == 200
        assert response.json() == expected_response


    @mock.patch('app.api.v1.routers.device.get_adb_client')
    def test_get_device_not_found(self, client_mock):
        device_mock = mock.MagicMock()
        device_mock.device.return_value = []
        client_mock.return_value = device_mock
        
        response = client.get("/device/emulator-5556/")
        assert response.status_code == 404

    @mock.patch('app.api.v1.routers.device.get_adb_client')
    @mock.patch('app.services.adb.client.device.PoweredDevice.screencap')
    def test_get_screenshot_successful(self, screencap_mock, client_mock):
        expected_response = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x002\x00\x00\x002\x08\x06\x00\x00\x00\x1e?\x88\xb1\x00\x00\x00XIDATx\x9c\xed\xcf\x01\t\xc00\x10\xc0\xc0_\xfd;\xa8\xd8\xcdD\xa1a\xdc)H\x9e=\xf3\xce\x0f\xac\xdb\x01\xa7\x18\xa91Rc\xa4\xc6H\x8d\x91\x1a#5Fj\x8c\xd4\x18\xa91Rc\xa4\xc6H\x8d\x91\x1a#5Fj\x8c\xd4\x18\xa91Rc\xa4\xc6H\x8d\x91\x1a#5Fj\x8c\xd4|\xb1]\x01\xfe\x16\x15\x91R\x00\x00\x00\x00IEND\xaeB`\x82'

        device_mock = mock.MagicMock()
        device_mock.device.return_value = PoweredDevice('client', 'emulador-5559')
        image = self._create_test_image().read()
        screencap_mock.return_value = image
        client_mock.return_value = device_mock
        
        response = client.get("/device/emulator-5559/screenshot/")
        assert response.status_code == 200
        assert response._content == expected_response

    @mock.patch('app.api.v1.routers.device.get_adb_client')
    @mock.patch('app.services.adb.client.device.PoweredDevice.get_log')
    def test_get_device_log_successful(self, log_mock, client_mock):
        log = 'Este es mi log'
        log_mock.return_value = log

        device_mock = mock.MagicMock()
        device_mock.device.return_value = PoweredDevice('client', 'emulador-5559')
        client_mock.return_value = device_mock
        
        response = client.get("/device/emulator-5559/logs/")
        print(response.status_code)
        assert response.status_code == 200
        assert response.json() == {
            'logs': log
        }

    @mock.patch('app.api.v1.routers.device.get_adb_client')
    @mock.patch('app.services.adb.client.device.PoweredDevice.open_app')
    def test_open_app_successful(self, message_mock, client_mock):
        message_mock.return_value = 'Open'
        device_mock = mock.MagicMock()
        device_mock.device.return_value = PoweredDevice('client', 'emulador-5559')
        client_mock.return_value = device_mock
        
        response = client.post(
            "/device/emulator-5559/open_app/",
            json={"app_id": "12345667"}
        )
        assert response.status_code == 200


    @mock.patch('app.api.v1.routers.device.get_adb_client')
    @mock.patch('app.services.adb.client.device.PoweredDevice.install')
    def test_install_app_successful(self, message_mock, client_mock):
        message_mock.return_value = 'Installed'
        device_mock = mock.MagicMock()
        device_mock.device.return_value = PoweredDevice('client', 'emulador-5559')
        client_mock.return_value = device_mock
        
        response = client.post(
            "/device/emulator-5559/install/",
            json={"path": "holahola"}
        )
        assert response.status_code == 200

