from typing import Optional

from App.Core.Network.Client import ClientConfig
from App.Core.Network.Protocol import CallRequest
from App.Core.Utils.Client import DocumentsRealSizes

from App.helpers import request


class DeviceService:
    def __init__(self,  config: ClientConfig):
        self.config = config

    def get_document(self, on_success: callable, on_error: callable, size: str, device: Optional[str] = None):
        x, y = DocumentsRealSizes.size(size)

        parameters = {'x': x, 'y': y}

        if device is not None:
            parameters['device'] = device

        return self.__request(CallRequest('scan', parameters=parameters), on_success, on_error)

    def get_devices(self, on_success: callable, on_error: callable, update: bool = False):
        _request = CallRequest('scan', ['devices'], {'update': update})

        return self.__request(_request, on_success, on_error)

    def __request(self, _request: CallRequest, on_success: callable, on_error: callable):
        return request(_request, self.config).then(on_success).catch(on_error)
